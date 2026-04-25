# Current plan

_Start date: 2026-04-21_
_First review: Sun 2026-05-04 (2 weeks in)_

## Strategic framing

The Noom/Simple history says the failure mode is clear: heavy tracking + rigid rules → ~6-month cliff → rebound. We design for sustainability from day one:

- **No calorie counting. No macro targets.** We track behaviors and the weight trend, not food arithmetic.
- **Minimum viable tracking.** Brief food log for pattern-spotting and accountability, not for math.
- **One lever at a time.** Three small experiments. Not a 40-item overhaul.
- **Social anchors untouched.** Friday lunch with friends, Saturday beers, Sunday margarita — those stay.
- **Joints are a constraint.** We are not touching the workout routine yet.

Target pace: ~1 lb/week (about 30 weeks to goal). Going faster is how we get the Noom rebound back. We're not doing that.

## First two weeks — three experiments

### 1. Pre-lunch reshape: protein primer, no prep-time chips

**Problem.** Pretzel chips + guac during lunch prep front-loads the meal with carbs and fat. By the time the turkey sandwich hits the plate, you've already eaten a second lunch, and the satiety signal catches up after the real lunch is also gone.

**Experiment.** When you walk into the kitchen at ~1pm, **eat a ~20g-protein primer first, before doing anything else.** Then prep lunch. **No pretzel chips + guac during prep.**

Primer options (pick based on what's in the fridge):
- 1 cup (240g) Greek yogurt (plain or low-sugar) — ~20g protein
- 1 cup cottage cheese — ~25g protein
- 2 hard-boiled eggs — ~13g (add a slice of cheese or a few almonds)
- 2–3 slices deli turkey rolled up with a wedge of cheese — ~20g
- 1 scoop whey/protein shake in water — ~25g
- 2 string cheese + 1 hard-boiled egg — ~20g

Lunch itself is unchanged for now.

**Why.** Blunts the ravenous drive so the actual lunch self-regulates. Replaces a mindless grazing habit with a small intentional one.

**Success signal.** You finish lunch not scanning the pantry.

### 2. Afternoon snack: one, planned, protein-forward — then kitchen closed

**Problem.** Afternoon snacks are a drift — granola bar here, pretzels there, some nuts, a few Cheez-Its. Small decisions compound into a meaningful second meal you didn't mean to eat.

**Experiment.** Designate **one** afternoon snack time (e.g., 3:30–4:00pm) and **one protein-forward item.** After that snack: kitchen closed until dinner. That line is the whole discipline.

Snack options:
- Greek yogurt + berries
- Cottage cheese + a small piece of fruit
- Turkey roll-ups (2–3 slices) + a few almonds
- Hard-boiled egg + apple
- Protein shake
- String cheese + an apple

Avoid: granola bars, pretzels, Cheez-Its, Nilla Wafers, handfuls of mixed nuts (a handful becomes six handfuls). Not forbidden foods — just not the 4pm default.

**Why.** Giving afternoon snacking a *shape* (one planned thing) beats trying to "just snack less." One real thing you eat on purpose is more satisfying than four drifts you half-register.

**Success signal.** Afternoon grazing stops. Dinner still feels like dinner, not a rescue.

### 3. Bedtime anchor

**Problem.** You're getting ~5.5 hours of unfragmented sleep. Chronic mild sleep debt pushes ghrelin up and leptin down — you'll feel more hungry, especially late-afternoon, and more reactive to stress cues. This quietly undermines everything else.

**Experiment.** **Lights-out by 11:15pm on at least 3 of the 5 weeknights (Sun–Thu).** No bigger overhaul. Just getting you off the hour-before-midnight cliff.

**Why.** Quiet leverage with high compounding. Even 30 extra minutes noticeably reduces afternoon snack intensity within a week. Also stress-protective.

**Success signal.** End of week 1: afternoon snack urge feels less insistent than it does today.

## What we are NOT doing yet

- Not cutting alcohol. Fri/Sat/Sun drinks stay.
- Not changing exercise. Knees/feet + current 4x/week routine stays. We'll revisit after week 2.
- Not counting calories or macros.
- Not eliminating Friday pizza or Sunday burritos.
- Not removing daughters' snacks from the house. That's their food. The job is making *your* choices easier, not sterilizing the kitchen.

Revisit list when we hit the first review:
- Weekday alcohol boundary (currently zero — keep it)
- Saturday beer dose (experiment: 2 → 1?)
- Swapping pizza Friday for something still joyful but less calorie-dense a few times a month
- Exercise progression: 2nd pull movement, KB load progression

### Exercise change (accelerated — added 2026-04-21)

Justin ordered Bodylastics resistance band set (arrives 2026-04-22) and may add a 35 lb KB. Starting **Wednesday 2026-04-22**, add one pull movement to his existing circuit:
- **Banded standing rows: 3 sets of 10–12 reps**, added to the existing circuit of KB squats + pushups + glute bridges
- Form cues: feet shoulder-width on the band, row to the ribs, elbows tracking back (not flared), squeeze shoulder blades at the top, slow eccentric
- Band tension: whichever lets him hit clean reps with ~2 in the tank on the last set
- Nothing else changes in the workout yet
- Rationale: routine is push/quad-heavy, no pull. Biggest imbalance for a WFH-desk person. One small addition, not a rewrite.

## Measurement

- **Weight:** Every morning post-void on the Withings. I pull via `python3 withings_sync.py`. Reported as **7-day trailing average**, not daily.
- **Food log:** Brief text — tell me as you eat, or at day's end. No portion sizes required unless meaningful. Photos welcome.
- **Hydration:** Running tally of water (ounces) throughout the day — just tell me as you drink. Starting aim: **~80 oz/day plain water**; coffee neither counts for nor against. No hard rule.
- **Sleep:** One number — time you turned out the light.
- **Workout:** Brief — what you did, how it felt.
- **Stress / mood:** 1–5, one number each.

All of it lands in `journal/YYYY-MM-DD.md`.

## Cadence

- **Daily check-in.** Few minutes. You drop in; I note and respond with at most one observation + one suggestion.
- **Friday or Saturday AM:** weekly review + dinner planning for the coming week, before you shop.
- **Every 2 weeks (first: Sun 2026-05-04):** look at the trend line, decide what to keep/drop/modify.

## Binge protocol

**Open.** We'll design this together the first time you feel the urge. Leaving it open on purpose — imposed protocols tend not to fire when the moment comes. Working hypothesis for the shape: a pre-committed pause (text me first, 15-minute walk, a glass of water), plus a "damage-control" ritual if it happens anyway so a slip doesn't turn into a three-day tailspin.

## Mid-week addition (2026-04-22): weekly template design

Justin disclosed he is a **template eater** — 11 years of identical school lunches. Strong habit-executor, poor daily-decider. This matches his 6-month burnout pattern: decision fatigue + tracking burden = collapse.

**Status (2026-04-25):** Template drafted and operational. See `weekly-template.md` — that is now the day-to-day source of truth. This file (`plan.md`) covers strategy and what's working; the template covers execution.

## Protein target (added 2026-04-25)

**Daily target: 150–180 g protein.** Calculated as 1.6–1.8 g/kg of goal body weight (100 kg).

Why this range:
- Cutting weight + lifting → protein protects lean mass during deficit
- Age 49 → anabolic resistance; older adults need more, not less
- Calculate against goal weight, not current — don't feed the fat you're trying to lose

**Estimated current intake: ~90–125 g/day** (under target by 30–60 g most days). Levers to close the gap without introducing tracking:
1. Bump primer to 8 oz cottage cheese (one full container)
2. Add HB egg or ½ cup cottage cheese to lunch salads
3. Keep dinner protein at 6–7 oz even when only moderately hungry; skip the carb side instead
4. Optional: protein shake on rest days or hectic afternoons

This is a target to aim toward, not a rule to track. The mistake is hovering at 90 g while training 4x/week.

## What's working (confirmed week 1)

- **Protein primer.** Day 3, Justin self-reported *"It prevents me from making stupid decisions about what I'm going to eat — I really feel it working."* Felt mechanism, not rule-following. PROTECT AT ALL COSTS.
- **Cottage cheese + diced strawberries** as primer default. Justin loves it.
- **Apple-as-dessert.** Clean meal-is-over signal; replaces pantry-drift at 7:45pm.
- **Self-regulating lunches.** Half sandwiches, taco bowls, big salads — Justin reports "comfortably full" / "very satisfied" without measuring.
- **Mexican lunch framework.** Cottage cheese in the car, ~10 chips, 2 tacos + one side, 2 beers — executed cleanly Friday 4/24.
- **Water cutoff at 8pm.** Eliminated 2am bathroom wakes.
- **Workout split Mon–Thu in a row** + active outdoor weekends. Honors his actual schedule.
- **Wednesday "real dinner" Thursday slot** matches the only weekday with cooking time.
- **"Friday flex" pattern** — parallel meal for family vs. Justin (e.g., spaghetti for them, leftovers for him). Avoids martyr meal AND kitchen sterilization.

## Household input (added 2026-04-25)

Wife joined as a stakeholder. Two effects:
1. She has independent weight-loss interest (no specific goals shared yet — open invitation)
2. She requested plant protein variety (chickpeas, lentils, etc.) — accurate critique that the original week was too chicken-heavy

Going forward: ≥1 plant-forward dinner per week, reduce chicken count, prioritize hybrid plates (e.g., chickpea curry + chicken on side) so Justin still hits protein target.

## Review log

_(Appended after each review.)_

### 2026-04-25 — Mid-week informal review (5 days in)

- Weight trend (Withings only): 247.5 → 246.1 → 244.6 lb (3 data points; noise-level, but direction is right). Home-scale start: 250.0.
- Adherence: high. Primer hit every day; one cookie incident (small, dismissed); Mexican lunch executed clean.
- Sleep: improving. Best night: Thu 11:00 lights-out clean. Friday: midnight (dance comp, family obligation > rule).
- Coach added: protein target 150–180 g/day; pivoted to weekly template; codified weigh-in / journaling rules; added wife as stakeholder; added air fryer + crockpot to equipment-aware planning.
- Open: Justin's wife's specific goals if she chooses to share; first plant-forward dinner to land in week 2; experiment with bigger primer or protein-shake top-up to close the protein gap.
