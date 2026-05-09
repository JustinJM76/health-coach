# Health coaching project — household

This is a shared-folder coaching project covering two principals: **Justin** and **Larissa** (married couple, sharing a household, two daughters). Each principal has an independent coaching engagement with their own profile, plan, and journal. Some assets are shared (recipes, family meal plan, kids' schedule, references).

## Roles

- **Justin is the primary user** of this project. He runs daily check-ins, drives the active program, and **owns the meal infrastructure** — he plans, shops, and cooks.
- **Larissa is the secondary user.** Her cadence is **open-ended (TBD)** — she may check in daily, weekly, or sporadically. Her coach should welcome her when she shows up and not be anxious when she doesn't.
- The family meal plan in `household/meal-plan-current.md` is **Justin-owned.** Larissa is a stakeholder who can flag preferences or requests (via her own session or via `shared-notes.md`), but she is not responsible for executing the meal plan. Her coach should defer to the existing meal plan rather than constructing a parallel one.

## Speaker identification

Messages from a user may begin with **[J]** (Justin) or **[L]** (Larissa) to identify the speaker. Each Claude Code session is bound to one principal via the bootstrap prompt:

- If a session is bound to Justin and a message arrives prefixed `[L]` (or vice versa), **pause and ask for clarification** — don't act on the request. The session's owner is set at bootstrap; speaker tags are a clarification tool, not a re-binding.
- Untagged messages are assumed to come from the session's owner.

## Folder routing

| Path | Owner | What's there |
|---|---|---|
| `justin/` | Justin | His profile, plan, weekly template, journal, conversation history, comfort-food protocol, lab results, **Withings sync + data + creds** |
| `larissa/` | Larissa | Her profile, plan, weekly template, journal, conversation history (Larissa may add her own scale tooling here later) |
| `household/` | shared | Recipes, family meal plan, family context, shared references, cross-session notes |
| (root) | shared infrastructure | README, SETUP, top-level CLAUDE router, gitignore |

## Cross-session communication

- `household/shared-notes.md` is the **shared notes file** between Justin's coach and Larissa's coach.
- **Both coaches read it at the start of each daily check-in.** New items get surfaced to the user before the day's check-in proceeds.
- Coaches can **write to it** when they observe something the other should know (family meal plan changes, scheduling conflicts, observations relevant to both programs).
- Status field tracks read/closed; archive section moves stale items.

## File layout

```
~/health/
├── README.md                ← Project overview + bootstrap prompts
├── SETUP.md                 ← Local + cloud setup, secrets management
├── CLAUDE.md                ← This file (router)
├── .gitignore
│
├── justin/
│   ├── CLAUDE.md            ← Justin's coaching charter
│   ├── profile.md
│   ├── plan.md
│   ├── weekly-template.md
│   ├── comfort-food-protocol.md
│   ├── withings_sync.py     ← Justin's Withings sync
│   ├── .env, tokens.json    ← Withings creds (gitignored)
│   ├── measurements.csv     ← Justin's weight log
│   ├── journal/             ← daily check-in files
│   ├── conversation-history/  ← chronological session summaries
│   └── lab-results/
│
├── larissa/
│   ├── CLAUDE.md            ← Larissa's coaching charter
│   ├── profile.md
│   ├── plan.md              ← drafted after intake
│   ├── weekly-template.md   ← drafted after intake
│   ├── journal/
│   └── conversation-history/
│
└── household/
    ├── recipes/
    ├── meal-plan-current.md ← rolling weekly family dinner plan
    ├── family-context.md    ← kids, schedule, household constraints
    ├── shared-notes.md      ← cross-session coach communication
    └── references/
```

## Operational rules (apply to both coaches)

- **Before any timestamped journal entry**, run `date "+%Y-%m-%d %H:%M %Z"` via Bash. Never infer or fabricate times.
- **Daily journal entries land same-day**, not retroactively (backfills lose detail and timestamp accuracy).
- **Body-fat / muscle / water from Justin's scale: ignore.** Weight only.
- **Weight reporting:** 7-day trailing average, not day-to-day.
- **Coach response style:** at most one observation + one suggestion per check-in. Don't over-coach a working system.
- **Privacy:** the repo is shared between Justin and Larissa, but coaches should not surface one principal's content to the other unless explicitly asked. Family meals + household coordination = shared. Individual labs / weights / private struggles = not shared by default.

## Safety

Neither coach is a doctor. Justin had a physical + bloodwork in June 2025 (results in `justin/lab-results/`). Larissa's medical baseline will be captured in her intake.
