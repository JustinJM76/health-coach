#!/usr/bin/env python3
"""Pull body-scale data from the Withings public API.

First run: opens a browser for OAuth2 authorization, saves tokens.json.
Subsequent runs: reuses / refreshes tokens silently, writes measurements.csv.
Stdlib only — no pip installs.
"""
import csv
import datetime as dt
import http.server
import json
import os
import sys
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
ENV_PATH = HERE / ".env"
TOKENS_PATH = HERE / "tokens.json"
CSV_PATH = HERE / "measurements.csv"

AUTH_URL = "https://account.withings.com/oauth2_user/authorize2"
SCOPE = "user.metrics,user.info"
START_DATE = dt.datetime(2025, 1, 1)

MEAS_TYPES = {
    1: "weight_kg",
    4: "height_m",
    5: "fat_free_mass_kg",
    6: "fat_ratio_pct",
    8: "fat_mass_kg",
    11: "heart_rate_bpm",
    76: "muscle_mass_kg",
    77: "hydration_kg",
    88: "bone_mass_kg",
}


REQUIRED_KEYS = (
    "WITHINGS_CLIENT_ID",
    "WITHINGS_SECRET",
    "WITHINGS_CALLBACK_URL",
    "WITHINGS_API_ENDPOINT",
)


def load_env(path):
    """Load Withings credentials.

    Order of precedence:
    1. Process environment variables (set by cloud runtime, GitHub Codespace
       secrets, GitHub Actions secrets, or `export` in a shell).
    2. Fallback to a local .env file at `path`, if present.

    Either source must provide all REQUIRED_KEYS.
    """
    env = {}
    # 1. Process env vars (cloud-friendly)
    for k in REQUIRED_KEYS:
        v = os.environ.get(k)
        if v:
            env[k] = v.strip()
    # 2. Fallback: .env file (local dev)
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            if k and k not in env:  # don't override env vars
                env[k] = v.strip().strip('"').strip("'")
    return env


def http_post(url, params, bearer=None):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    if bearer:
        req.add_header("Authorization", f"Bearer {bearer}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    captured = {}

    def log_message(self, *a, **kw):
        pass

    def do_GET(self):
        q = urllib.parse.urlparse(self.path).query
        params = dict(urllib.parse.parse_qsl(q))
        if params:
            CallbackHandler.captured.update(params)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if "code" in params:
            body = b"<h2>Withings authorization captured.</h2><p>You can close this window.</p>"
        else:
            body = b"<h2>Waiting for Withings callback...</h2>"
        self.wfile.write(body)


def run_oauth_flow(env):
    state = os.urandom(8).hex()
    params = {
        "response_type": "code",
        "client_id": env["WITHINGS_CLIENT_ID"],
        "scope": SCOPE,
        "redirect_uri": env["WITHINGS_CALLBACK_URL"],
        "state": state,
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    parsed = urllib.parse.urlparse(env["WITHINGS_CALLBACK_URL"])
    host = parsed.hostname or "localhost"
    port = parsed.port or 80
    server = http.server.HTTPServer((host, port), CallbackHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    print("Open this URL in your browser to authorize:\n")
    print(f"  {auth_url}\n")
    try:
        import webbrowser
        webbrowser.open(auth_url)
    except Exception:
        pass

    deadline = time.time() + 300
    while time.time() < deadline and "code" not in CallbackHandler.captured:
        time.sleep(0.5)
    server.shutdown()

    if "code" not in CallbackHandler.captured:
        raise SystemExit("Timed out waiting for authorization.")
    if CallbackHandler.captured.get("state") != state:
        raise SystemExit("State mismatch — possible CSRF, aborting.")

    resp = http_post(f"{env['WITHINGS_API_ENDPOINT']}/v2/oauth2", {
        "action": "requesttoken",
        "client_id": env["WITHINGS_CLIENT_ID"],
        "client_secret": env["WITHINGS_SECRET"],
        "grant_type": "authorization_code",
        "code": CallbackHandler.captured["code"],
        "redirect_uri": env["WITHINGS_CALLBACK_URL"],
    })
    if resp.get("status") != 0:
        raise SystemExit(f"Token exchange failed: {resp}")
    return save_tokens(resp["body"])


def refresh_tokens(env, tokens):
    resp = http_post(f"{env['WITHINGS_API_ENDPOINT']}/v2/oauth2", {
        "action": "requesttoken",
        "client_id": env["WITHINGS_CLIENT_ID"],
        "client_secret": env["WITHINGS_SECRET"],
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
    })
    if resp.get("status") != 0:
        raise SystemExit(f"Token refresh failed: {resp}")
    return save_tokens(resp["body"])


def save_tokens(body):
    tokens = {
        "access_token": body["access_token"],
        "refresh_token": body["refresh_token"],
        "expires_at": int(time.time()) + int(body["expires_in"]) - 60,
        "userid": body.get("userid"),
        "scope": body.get("scope"),
    }
    TOKENS_PATH.write_text(json.dumps(tokens, indent=2))
    os.chmod(TOKENS_PATH, 0o600)
    return tokens


def get_tokens(env):
    if TOKENS_PATH.exists():
        tokens = json.loads(TOKENS_PATH.read_text())
        if tokens.get("expires_at", 0) > time.time():
            return tokens
        print("Access token expired, refreshing...", file=sys.stderr)
        return refresh_tokens(env, tokens)
    return run_oauth_flow(env)


def fetch_measurements(env, tokens):
    url = f"{env['WITHINGS_API_ENDPOINT']}/measure"
    meastypes = ",".join(str(k) for k in MEAS_TYPES)
    groups = []
    offset = None
    while True:
        params = {
            "action": "getmeas",
            "meastypes": meastypes,
            "category": 1,
            "startdate": int(START_DATE.timestamp()),
        }
        if offset is not None:
            params["offset"] = offset
        resp = http_post(url, params, bearer=tokens["access_token"])
        if resp.get("status") != 0:
            raise SystemExit(f"getmeas failed: {resp}")
        body = resp["body"]
        groups.extend(body.get("measuregrps", []))
        if body.get("more") and body.get("offset"):
            offset = body["offset"]
        else:
            break
    return groups


def write_csv(groups):
    rows = []
    for g in groups:
        row = {
            "date_iso": dt.datetime.fromtimestamp(g["date"]).isoformat(),
            "date_epoch": g["date"],
            "grpid": g["grpid"],
        }
        for m in g.get("measures", []):
            name = MEAS_TYPES.get(m["type"], f"type_{m['type']}")
            row[name] = m["value"] * (10 ** m["unit"])
        rows.append(row)
    rows.sort(key=lambda r: r["date_epoch"])
    cols = ["date_iso", "date_epoch", "grpid"] + list(MEAS_TYPES.values())
    with CSV_PATH.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return rows


def main():
    env = load_env(ENV_PATH)
    for key in REQUIRED_KEYS:
        if not env.get(key):
            raise SystemExit(
                f"Missing {key}. Set it in the process environment "
                f"(cloud secret) or in {ENV_PATH} (local .env file)."
            )

    tokens = get_tokens(env)
    print(f"Authorized as Withings user {tokens.get('userid')}.")

    groups = fetch_measurements(env, tokens)
    rows = write_csv(groups)
    print(f"Wrote {len(rows)} measurement groups to {CSV_PATH}")
    if rows:
        first = dt.datetime.fromtimestamp(rows[0]["date_epoch"]).strftime("%Y-%m-%d")
        last = dt.datetime.fromtimestamp(rows[-1]["date_epoch"]).strftime("%Y-%m-%d")
        weights = [r["weight_kg"] for r in rows if r.get("weight_kg") is not None]
        print(f"Date range: {first} → {last}")
        if weights:
            print(f"Weights: {len(weights)} readings, min {min(weights):.1f} kg, "
                  f"max {max(weights):.1f} kg, latest {weights[-1]:.1f} kg")


if __name__ == "__main__":
    main()
