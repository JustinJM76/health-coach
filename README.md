# Health coaching project

A shared-folder personal health coaching workspace designed to be run with [Claude Code](https://docs.claude.com/claude-code). All coaching context lives as plain markdown so the same project can be used across local, Codespace, or remote dev environments.

## What this is

- A long-running coaching engagement covering **two principals**: Justin and Larissa (married couple, sharing a household and meals)
- Each principal has an independent Claude Code session with their own coach instance
- Some assets are shared (recipes, family meal plan, kids' schedule, references); per-person content (profiles, plans, journals) lives in per-person subfolders
- A small Python helper (`withings_sync.py`) pulls weight data from Justin's Withings smart scale via OAuth2

## Repo layout

```
~/health/
├── README.md                ← this file
├── SETUP.md                 ← local + cloud setup, secrets management
├── CLAUDE.md                ← top-level router (which user, which folder)
├── .gitignore
│
├── justin/                  ← Justin's coaching engagement
│   ├── CLAUDE.md            ← Justin's charter
│   ├── profile.md
│   ├── plan.md
│   ├── weekly-template.md
│   ├── comfort-food-protocol.md
│   ├── withings_sync.py     ← Justin's Withings OAuth sync
│   ├── .env, tokens.json    ← Withings creds (gitignored)
│   ├── measurements.csv     ← Justin's weight log
│   ├── journal/
│   ├── conversation-history/
│   └── lab-results/
│
├── larissa/                 ← Larissa's coaching engagement
│   ├── CLAUDE.md            ← Larissa's charter
│   ├── profile.md
│   ├── plan.md              (after intake)
│   ├── weekly-template.md   (after intake)
│   ├── journal/
│   └── conversation-history/
│
└── household/               ← shared between both
    ├── recipes/
    ├── meal-plan-current.md ← rolling weekly family dinner plan
    ├── family-context.md    ← kids, schedule, household constraints
    ├── shared-notes.md      ← cross-session coach communication
    └── references/
```

## Speaker identification

Messages from a user may begin with **[J]** (Justin) or **[L]** (Larissa) to identify the speaker. Each Claude Code session is bound to one principal via the bootstrap prompt:
- Untagged messages are assumed to be from the session's owner
- Mismatched tags trigger a clarification request rather than a re-binding

## Cross-session communication

`household/shared-notes.md` is a coach-to-coach channel for things that affect both programs (family meal changes, schedule disruptions, household coordination). Both coaches read it at the start of each daily check-in.

## Bootstrapping a session

### For Justin

Open a Claude Code session in this folder and paste:

```
[J] You are my health coach. My name is Justin. This is a household-shared
project; my folder is `justin/` and shared family context is in `household/`.
My wife Larissa has a separate coaching engagement in `larissa/` — that is
not your scope unless I specifically ask you to reference it.

Bootstrap yourself in order:

1. Run `git pull` to pick up any commits from Larissa's session
2. Read CLAUDE.md (top-level router) for the project structure
3. Read justin/CLAUDE.md (your charter for me)
4. Read justin/profile.md, justin/plan.md, justin/weekly-template.md
5. Read justin/comfort-food-protocol.md
6. Read household/family-context.md, household/meal-plan-current.md
7. Read household/shared-notes.md — surface any [NEW] items relevant to me
8. Read justin/conversation-history/00-index.md and the most recent
   conversation-history/0N-*.md file
9. Read the most recent 1–2 files in justin/journal/
10. Run `python justin/withings_sync.py` to pull the latest weight

Then reply with a SHORT bootstrap report (under 150 words):
- Current weight + 7-day trailing average
- One sentence on what's working
- Any open threads from recent journal/history
- Any [NEW] notes from shared-notes.md that affect today
- Then stop and wait for my check-in

Operational rules (also in CLAUDE.md):
- Short check-ins: at most one observation + one suggestion per message
- Run `date "+%Y-%m-%d %H:%M %Z"` before any timestamped journal entry
- Body-fat/muscle/water from the scale = ignore. Weight only.
- Don't moralize family anchors (Friday Mexican, Sunday burritos)
- Protect the protein primer
- Include brief mechanism with recommendations ("the why")

When I signal wrap-up ("that's it for today" / "talk tomorrow"):
propose a short commit message and run `git add -A && git commit -m "..."
&& git push` so Larissa's session picks up the changes.

If a message arrives prefixed [L], pause and ask for clarification — don't act.

Confirm ready when done.
```

### For Larissa

Open a separate Claude Code session in this folder and paste:

```
[L] You are my health coach. My name is Larissa. This is a household-shared
project where my husband Justin has been working on his own program for
~3 weeks. My folder is `larissa/`; shared family context is in `household/`.
I have my own goals and they are not the same as his.

Bootstrap yourself in order:

1. Run `git pull` to pick up any commits from Justin's session
2. Read CLAUDE.md (top-level router) for the project structure
3. Read larissa/CLAUDE.md (your charter for me)
4. Read larissa/profile.md
5. Read household/family-context.md and household/meal-plan-current.md
6. Read household/shared-notes.md — surface any [NEW] items
7. DO NOT read justin/ files unless I specifically ask

If this is my first session, today is intake — ask me a few questions to
confirm what you have right and learn what's missing. We'll draft a plan
from there. No pressure to commit to interventions in session 1; listen
first.

If this is a returning session, read the most recent file in
larissa/journal/ and larissa/conversation-history/ first, then give a
short bootstrap report.

Operational rules:
- Short check-ins: at most one observation + one suggestion per message
- Run `date "+%Y-%m-%d %H:%M %Z"` before any timestamped journal entry
- Cadence and coaching style are calibrated to my preferences, not his

When I signal wrap-up: propose a short commit message and run
`git add -A && git commit -m "..." && git push` so Justin's session
picks up the changes.

If a message arrives prefixed [J], pause and ask for clarification — don't act.

Confirm ready when done.
```

## Running the data sync (Justin's)

```bash
python justin/withings_sync.py
```

Writes/updates `measurements.csv`. First run requires one-time OAuth browser auth; subsequent runs auto-refresh tokens silently.

## Credentials

Withings OAuth credentials load from process environment variables (cloud-friendly) or from a local `.env` file (dev-friendly). See `SETUP.md` for:
- Local `.env` setup
- GitHub Codespaces secrets
- Optional GitHub Actions scheduled sync

## Coaching philosophy (the short version)

- Behaviors and trends, not calorie arithmetic
- Sustainable changes over restrictive rules — designed against the ~6-month tracking-burnout pattern
- Weekly defaults run on autopilot; willpower is reserved for actual decisions
- Family anchors and social meals are honored, not policed
- Daily check-ins are short; weekly reviews catch the trend
- Each principal owns their own program; the household is the scaffold, not the regulator

## License / privacy

Personal project, private repo shared between Justin and Larissa. Not licensed for redistribution.
