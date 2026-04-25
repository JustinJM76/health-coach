# Health coaching project

A personal health coaching workspace designed to be run with [Claude Code](https://docs.claude.com/claude-code). All coaching context, plans, profiles, and daily check-ins live as plain markdown so the same project can be used across local, Codespace, or remote dev environments.

## What this is

- A long-running coaching engagement between the project owner and a Claude-powered coach
- All program state — plans, profiles, schedules, daily journals, and prior conversations — is captured as markdown that any new Claude instance can read to pick up where the last one left off
- A small Python helper (`withings_sync.py`) pulls weight data from a Withings smart scale via OAuth2

## Repo layout

| Path | Purpose |
|---|---|
| `CLAUDE.md` | **Start here.** Project instructions and operational rules for the Claude coach. |
| `profile.md` | Static profile (demographics, labs, history, preferences). Updated as new info surfaces. |
| `plan.md` | Strategy + current intervention plan + "what's working" log. |
| `weekly-template.md` | Operational Mon–Sun template (workouts, meals, anchors). Day-to-day source of truth. |
| `journal/YYYY-MM-DD.md` | One file per daily check-in. |
| `conversation-history/` | Chronological summaries of past coaching sessions. Read these to recover context if a long session was lost. |
| `measurements.csv` | Withings weight log. Synced via `withings_sync.py`. |
| `withings_sync.py` | OAuth2 client + measurement puller. Reads creds from env vars or `.env`. |
| `lab-results/` | Bloodwork PDFs (gitignored on the project owner's discretion). |
| `SETUP.md` | Local setup, secrets management, GitHub migration guide. |

## Bootstrapping a new Claude Code session

When a new Claude instance opens this project, point it at the docs in this order so it gets full context efficiently:

1. **`CLAUDE.md`** — overall instructions, role, file map, coaching approach, operational rules.
2. **`profile.md`** — who the project owner is and key facts that don't change often.
3. **`plan.md`** — current strategy, what's working, protein target, etc.
4. **`weekly-template.md`** — the week's defaults. This is the operational doc.
5. **`conversation-history/00-index.md`** → most recent daily summary — to understand current momentum and any open threads.
6. **Most recent `journal/YYYY-MM-DD.md`** — most recent check-in detail.

A typical opening prompt to a fresh Claude session:

> Read `CLAUDE.md`, `profile.md`, `plan.md`, `weekly-template.md`, the latest file in `conversation-history/`, and the latest file in `journal/`. Then I'll do my daily check-in.

## Running the data sync

Before each daily check-in, sync the latest weigh-in:

```bash
python withings_sync.py
```

The script writes/updates `measurements.csv` and prints a one-line summary of the date range and latest weight. First run requires a one-time OAuth browser authorization; subsequent runs auto-refresh tokens silently.

## Credentials

Withings OAuth credentials are required for the sync. They're loaded from process environment variables (cloud-friendly) or from a local `.env` file (dev-friendly). The `.env` and `tokens.json` files are gitignored and **never** committed.

See **`SETUP.md`** for:
- Local `.env` setup
- GitHub Codespaces secrets
- Optional GitHub Actions scheduled sync
- Migrating an existing setup to the cloud

## Coaching philosophy (the short version)

- Behaviors and trends, not calorie arithmetic
- Sustainable changes over restrictive rules — designed against the ~6-month tracking-burnout pattern
- Weekly defaults run on autopilot; willpower is reserved for actual decisions
- Family anchors and social meals are honored, not policed
- Daily check-ins are short; weekly reviews catch the trend

Detailed coaching style notes are in `CLAUDE.md`.

## License / privacy

Personal project, private repo. Not licensed for redistribution.
