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
