# Setup — local + cloud

This project tracks Justin's coaching program. The bulk of it is plain markdown that travels fine. The one moving part is the Withings OAuth integration, which needs credentials and tokens that must NOT land in the repo.

## Repository contents (what gets committed)

- All `.md` files (top-level `CLAUDE.md`, `README.md`, this file, plus all `.md` files under `justin/`, `larissa/`, `household/`)
- `justin/withings_sync.py` — Justin's Withings OAuth sync
- `justin/measurements.csv` — synced weight log (not secret; useful to have committed)
- `justin/lab-results/` — your bloodwork PDFs (PHI; your call whether to commit)
- `.gitignore`

## NEVER committed (in .gitignore)

- `.env` (and `.env.local`) — Withings client ID and secret. Lives at `justin/.env`. The gitignore pattern matches `.env` anywhere in the tree.
- `tokens.json` — OAuth access + refresh tokens. **Currently NOT in .gitignore by Justin's choice** so the cloud bootstrap path works. If that changes, re-add the line.
- `.DS_Store`, `__pycache__/`, etc.

## Migrating to a private GitHub repo

### Step 1 — Create the repo (locally first, push second)

From `~/health`:

```bash
cd ~/health
git init
git add .
git status   # SANITY CHECK: confirm .env and tokens.json are NOT staged
git commit -m "Initial commit — health coaching project"
```

Then on github.com, create a **private** repository called `health` (or whatever). Don't initialize it with a README — you already have content. GitHub will show the push commands; use the SSH or HTTPS form:

```bash
git remote add origin git@github.com:YOUR_USERNAME/health.git
git branch -M main
git push -u origin main
```

### Step 2 — Verify nothing leaked

After pushing, browse the repo on github.com and confirm:
- No `.env` file visible (anywhere — should be gitignored from any directory)
- `justin/measurements.csv` is there (this is fine — it's your weight log, not a credential)
- `justin/lab-results/` PDFs — confirm these are intentional (they contain PHI)

If you accidentally committed `.env`: that credential is now compromised. Rotate it immediately — regenerate the Withings client secret on the Withings developer portal, then redo the OAuth dance.

## Running from the cloud (Claude Code in a remote dev environment)

The Withings credentials need to be available as environment variables to the cloud runtime. `withings_sync.py` checks process environment first, then falls back to `.env` — so set the env vars in the cloud and the script just works.

### Required environment variables

| Name | Value (from your local `.env`) |
|---|---|
| `WITHINGS_CLIENT_ID` | (from Withings developer portal) |
| `WITHINGS_SECRET` | (the client secret) |
| `WITHINGS_CALLBACK_URL` | (the redirect URL you registered with Withings) |
| `WITHINGS_API_ENDPOINT` | `https://wbsapi.withings.net` |

### Option A — GitHub Codespaces (recommended)

1. On the GitHub repo page → **Settings → Secrets and variables → Codespaces → New repository secret**
2. Add the four variables above, one per secret
3. Create a Codespace from the repo: **Code → Codespaces → Create codespace on main**
4. Once the Codespace boots, secrets are available as env vars automatically. Test:
   ```bash
   echo $WITHINGS_CLIENT_ID    # should print your client ID
   python justin/withings_sync.py     # should run; first run needs OAuth (see "First-run OAuth" below)
   ```
5. `tokens.json` will be written into the Codespace's persistent workspace volume. It survives across Codespace stop/start cycles for the same Codespace, but is NOT pushed to git (it's gitignored).

### Option B — GitHub Actions (scheduled syncs only, no Claude Code)

Useful if you just want measurements to auto-sync. Not relevant if Claude Code is your primary access path.

```yaml
# .github/workflows/sync.yml
name: Withings sync
on:
  schedule:
    - cron: "0 13 * * *"   # 9am EDT-ish daily
  workflow_dispatch:
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - name: Sync
        env:
          WITHINGS_CLIENT_ID: ${{ secrets.WITHINGS_CLIENT_ID }}
          WITHINGS_SECRET: ${{ secrets.WITHINGS_SECRET }}
          WITHINGS_CALLBACK_URL: ${{ secrets.WITHINGS_CALLBACK_URL }}
          WITHINGS_API_ENDPOINT: ${{ secrets.WITHINGS_API_ENDPOINT }}
        run: python justin/withings_sync.py
      - name: Commit measurements
        run: |
          git config user.name "withings-bot"
          git config user.email "actions@github.com"
          git add justin/measurements.csv
          git diff --staged --quiet || git commit -m "sync: $(date -u +%F)"
          git push
```

This requires a refresh token already present — see "First-run OAuth" below — and a way to persist the rotating refresh token. Doable but fiddly. For now, Option A is the path.

### Option C — Run locally only, sync the CSV manually

Simplest fallback. Keep doing what you're doing on your laptop. The CSV gets pushed when you commit. Cloud Claude Code reads the committed CSV but doesn't run `withings_sync.py` itself. You lose live syncs from cloud sessions but no security complications.

### First-run OAuth (one-time)

The OAuth flow needs a browser to authorize, which is awkward in a headless cloud environment. Two clean approaches:

1. **Do the OAuth dance locally first**, then upload `tokens.json` to the cloud as a one-time bootstrap:
   - Run `python justin/withings_sync.py` locally → completes browser auth → writes `tokens.json`
   - Copy the `tokens.json` contents into a Codespace secret, e.g. `WITHINGS_TOKENS_JSON`
   - On the cloud, write a tiny startup step: `echo "$WITHINGS_TOKENS_JSON" > tokens.json` before running the sync
   - From there, the script auto-refreshes the token silently

2. **Always re-do OAuth in the cloud** when the refresh token expires (rare — Withings refresh tokens are long-lived). The Codespace can host the temporary callback if you forward the local port; clunky but works.

Practical recommendation: do (1) once. Refresh tokens are durable; you should rarely need to redo the dance.

## Quick checklist for the migration

- [ ] `cd ~/health && git init && git add . && git status`
- [ ] **Confirm `.env` and `tokens.json` are NOT in `git status` output**
- [ ] `git commit -m "Initial commit"`
- [ ] Create private repo on GitHub
- [ ] `git remote add origin <url> && git push -u origin main`
- [ ] Browse repo on github.com, confirm no secrets leaked
- [ ] In repo Settings → Secrets → Codespaces, add the 4 Withings vars
- [ ] (Optional) Add `WITHINGS_TOKENS_JSON` secret containing the JSON contents of your local `tokens.json`
- [ ] Spin up a Codespace, run `python justin/withings_sync.py`, confirm it pulls measurements

## When in doubt

If anything looks like it might leak a secret (a file unexpectedly staged, a script printing tokens), STOP and ask. It's much easier to not commit a secret than to clean one up after the fact.

## Pi home-server setup — always-on coach sessions (May 2026)

The Pi runs two persistent Claude Code Remote Control sessions (one per coach) as systemd user services. They're reachable from the Claude desktop and iOS apps under the names `Health Coach - Justin` and `Health Coach - Larissa`. Conversation context survives reboots via UUID-pinned local sessions.

**Files (NOT in repo — live on the Pi only):**

`~/.local/bin/coach-remote-control` (chmod +x):
```bash
#!/bin/bash
# First run: --session-id (creates). Subsequent: --resume (preserves history).
set -euo pipefail
[[ $# -eq 2 ]] || { echo "Usage: $0 <uuid> <name>" >&2; exit 64; }
UUID="$1"; NAME="$2"
CLAUDE_BIN="${CLAUDE_BIN:-/home/justin/.local/bin/claude}"
SESSION_FILE="$HOME/.claude/projects/$(pwd | sed 's|/|-|g')/${UUID}.jsonl"
if [[ -f "$SESSION_FILE" ]]; then
    exec "$CLAUDE_BIN" --dangerously-skip-permissions --resume "$UUID" --remote-control "$NAME"
else
    exec "$CLAUDE_BIN" --dangerously-skip-permissions --session-id "$UUID" --remote-control "$NAME"
fi
```

`~/.config/systemd/user/claude-justin.service` (Larissa's is identical, swap dir/UUID/name):
```ini
[Unit]
Description=Claude Code Remote Control - Justin's coach
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/justin/health-coach/justin
Environment=TERM=xterm-256color
ExecStart=/usr/bin/script -qfc "/home/justin/.local/bin/coach-remote-control <UUID> 'Health Coach - Justin'" /dev/null
Restart=always
RestartSec=10
StandardInput=null

[Install]
WantedBy=default.target
```

**Pinned UUIDs (current Pi):**
- Justin: `d5f7e107-6f15-42d9-8cac-29b38f69f9a7`
- Larissa: `6a71ec10-95f3-4b22-a02b-15a3db59b3ab`

Fresh installs should generate new ones: `cat /proc/sys/kernel/random/uuid`.

**Why each piece:**
- `script -qfc ... /dev/null` — Claude refuses interactive mode without a TTY; `script` allocates one.
- Stable UUID + wrapper — Remote Control URL rotates per restart, but the local `<uuid>.jsonl` is the actual conversation transcript. Pinning the UUID and using `--resume` after first start preserves history.
- `--dangerously-skip-permissions` — no permission prompts when driving from phone. Trade-off accepted; sessions are scoped to their own coach directories.

**One-time enable:**
```bash
mkdir -p ~/.config/systemd/user
# write the two .service files and the wrapper
chmod +x ~/.local/bin/coach-remote-control
systemctl --user daemon-reload
systemctl --user enable --now claude-justin.service claude-larissa.service
sudo loginctl enable-linger justin   # so services start at boot without a login
```

**Verify:** `systemctl --user is-active claude-justin claude-larissa` → both `active`. Sessions appear in claude.ai/code by name within ~10 seconds.

**Logs (ANSI-stripped):**
```bash
journalctl _SYSTEMD_USER_UNIT=claude-justin.service -f --all -o cat | sed 's/\x1b\[[0-9;]*[mGKHJABCDsu]//g'
```

**Reset a coach session (lose history):**
```bash
systemctl --user stop claude-justin
rm ~/.claude/projects/-home-justin-health-coach-justin/*.jsonl
systemctl --user start claude-justin
```

**Known limitation:** every service restart leaks one Remote Control entry into the desktop/iOS app session list. No cleanup tooling ships as of May 2026 (Anthropic issues #50884, #50496). Pick the active entry by name; ignore the duplicates.
