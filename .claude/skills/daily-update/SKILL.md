---
description: Daily plan synthesis. Pulls fresh data, reviews recent context, writes today's plan to plans/YYYY-MM-DD.md, and commits. Invoked by cron at 6AM and 10AM in each principal's directory.
disable-model-invocation: true
---

# Daily update

You are the coach (Justin's or Larissa's, whichever folder you're in — your `CLAUDE.md` charter has already loaded). This is an **autonomous cron-fired run**, not an interactive session. Be efficient, write today's plan, and commit. No conversational output is needed; the only artifact that matters is the plan file you write.

## Step 1 — Identify principal and date

- Determine which principal you are coaching by reading the current directory: `justin/` → Justin, `larissa/` → Larissa.
- Get today's date in the user's local timezone:
  ```
  date "+%Y-%m-%d"
  ```
- Stash both as `$PRINCIPAL` and `$DATE` for use below.

## Step 2 — Sync the repo (defensive)

Run `git pull --rebase --autostash` to fetch other devices' commits without being blocked by unstaged in-flight edits (household notes, rotated tokens, etc.). `--autostash` will save and restore them transparently.

Only stub-and-exit if the pull surfaces an **actual merge conflict** (rebase aborts mid-flight, leaves the tree in conflicted state). In that case write `plans/$DATE.md` with `motd: "Plan generation paused — sync conflict, please resolve."` and exit. Don't auto-resolve.

If pull succeeds with stashed/restored changes, proceed normally. If pull fails for a network reason (origin unreachable), proceed normally with local state — the eventual push at Step 7 will likely fail too, and the next run will catch up.

## Step 3 — Pull fresh data (Justin only)

If `$PRINCIPAL == justin`:
- Run `python withings_sync.py` from the principal's directory. This updates `measurements.csv` with any new weigh-ins.
- If it fails (network, expired token), continue without — note the failure in the `notes` field of today's plan.

If `$PRINCIPAL == larissa`: skip — she has no scale integration.

## Step 4 — Read context

Read these files (skip silently if missing):

- `CLAUDE.md` — the charter (already in context, but re-read if you need specifics)
- `profile.md`
- `plan.md`
- `weekly-template.md`
- `comfort-food-protocol.md` (Justin only)
- The five most recent files in `journal/` (sorted by filename, descending)
- The five most recent files in `plans/` (excluding today's, if it exists)
- `../household/meal-plan-current.md`
- `../household/shared-notes.md`
- `../household/family-context.md` (only if relevant to today)

For Justin: also read the last ~14 lines of `measurements.csv` to compute weight trend. When computing `trailing_7d_avg_lb`:

- **Morning weigh-ins only.** The protocol is a morning, fasted weigh-in (after coffee + BM). **Exclude any read timestamped at or after noon** — a midday/evening step-on is not trend data and will skew the average. Note the exclusion in `notes` if it affects the number.
- **Same-morning multiples:** 2 reads → average them; 3+ → discard the outlier, average the rest (cocked-foot scale artifact).
- **Trailing average = 7-calendar-day window** (today + prior 6 calendar days), averaging the valid daily values that fall inside it. During multi-day gaps (e.g. travel) the window simply holds fewer points — use what's there and note the small n rather than reaching further back in time.

## Step 5 — Synthesize today's plan

Today is `$DATE`. Look at the day-of-week (e.g. `date "+%A"`) and pull from `weekly-template.md`. Adjust based on:

- **Adherence patterns from recent journal entries.** If Justin skipped Wednesday's workout three weeks running, today's Wed plan should not pretend that's not happening — propose a smaller alternative.
- **Recent weight trend** (Justin). 7-day trailing average up or down? Plan reflects this without overreacting (per CLAUDE.md: "don't react to daily weight noise").
- **Open items in `shared-notes.md`** that affect today (meal plan changes, scheduling).
- **Recent plans you wrote.** Don't repeat the exact same MOTD; vary the framing.

The plan should be concrete, short, and respectful of the coaching style in CLAUDE.md (one observation + one suggestion, not a wall of text).

## Step 6 — Write `plans/$DATE.md`

Write the file with this YAML frontmatter schema, followed by an optional free-form body. Required fields are marked. Use `null` for unknown values, never fabricate.

```yaml
---
date: 2026-05-10                          # required, ISO format
principal: justin                          # required: justin | larissa
weekday: Sunday                            # required
motd: "One short, specific line."          # required, ≤120 chars, no surrounding quotes inside
weight:                                    # null for Larissa pre-scale
  latest_lb: 248.4
  latest_date: 2026-05-09
  trailing_7d_avg_lb: 249.1
  trend_vs_prior_7d_lb: -0.4               # negative = trending down
goals:                                     # array, can be empty
  - title: "250 → 220 lb"
    status: on-track                       # on-track | watch | off-track | tbd
    note: "From 250 start; current 7-day avg 249.1."
workout:                                   # null if rest day or pre-intake
  title: "Resistance + KB + elliptical (Tue)"
  description: "Brief 1-2 sentence summary of today's workout."
  details_path: weekly-template.md         # relative to principal's dir; renderer makes a link
meals:                                     # array; each has meal, description, recipe_path?
  - meal: breakfast
    description: "Greek yogurt + berries (post-fast — Justin breaks fast at 1pm)."
    recipe_path: null
  - meal: lunch
    description: "..."
    recipe_path: null
  - meal: dinner
    description: "White chicken chili (family dinner per meal plan)."
    recipe_path: ../household/recipes/white-chicken-chili.md
tasks:                                     # array of strings; can be empty
  - "Log weight before lunch."
  - "Drop a note in shared-notes if you want a different protein on Thursday."
notes: ""                                  # free-form, optional, surfaced to dashboard
generated_at: 2026-05-10T06:00:00-04:00    # required, ISO datetime
generated_by: daily-update-skill           # required (always this string)
---

(Optional free-form body in markdown — surfaced as a "Coach's note" block in the dashboard.)
```

### Schema rules

- All paths are relative to the **principal's directory** (e.g. `weekly-template.md`, `../household/recipes/x.md`). The renderer translates these into links.
- For Larissa pre-intake: many fields will be `null` or empty arrays. That's fine — produce honest sparse data, not fabricated content. Still write a useful MOTD and a `tasks` array if there's anything practical.
- Never invent recipe paths. If the meal isn't tied to a recipe in `household/recipes/`, set `recipe_path: null`.
- MOTD: vary the energy. Some days clever, some days direct, some days specific to today's plan. Avoid generic platitudes.

## Step 7 — Commit and push

If the environment variable `DAILY_UPDATE_DRY_RUN=1` is set, **skip this step entirely** (dry-run mode for testing). Otherwise:

```bash
git add plans/$DATE.md ../justin/measurements.csv 2>/dev/null
git -c user.name="daily-update-bot" -c user.email="bot@health-coach.local" commit -m "daily-update: $PRINCIPAL plan for $DATE" --allow-empty
git push
```

If push fails (network, etc.), don't retry — the next cron run will catch up. Just log the failure to stderr.

## Step 8 — Done

No further output. The cron wrapper will run the dashboard renderer next.
