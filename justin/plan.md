# Current plan

_Start date: 2026-04-21_
_First review: Sun 2026-05-04 (2 weeks in)_

## Strategic framing

The Noom/Simple history says the failure mode is clear: heavy tracking + rigid rules → ~6-month cliff → rebound. We design for sustainability from day one:

**Goal framing:** 220 lb is the *current* goal, set 2026-04-21. As of the 5/17 review, Justin is open to a Phase 2 (target ~210 or ~200) depending on body composition, energy, lifts, and felt experience at 220. Approach: don't slow approaching 220, but at 220 explicitly shift to maintenance for 3–4 weeks (let the body settle out of deficit) before deciding Phase 2. Adds at the 220 checkpoint: waist circumference (one cheap measurement that informs composition decisions better than scale alone).



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

_Revised 2026-06-16 — see the Acceleration-phase review-log entry and `CLAUDE.md` for the current cadence (3×/day, rotating health probes via `checkin_variety.py`, more verbose/engaged, Outlive "why" ~2×/wk). The lighter original is kept below for history._

- **Daily check-in.** Few minutes. You drop in; I note and respond. _(Superseded: was "one observation + one suggestion"; acceleration phase loosened this to fuller engagement.)_
- **Friday or Saturday AM:** weekly review + dinner planning for the coming week, before you shop.
- **Every 2 weeks (first: Sun 2026-05-04):** look at the trend line, decide what to keep/drop/modify.

## Binge / comfort-food protocol — DRAFTED 2026-04-29

**Designed.** See `comfort-food-protocol.md`.

Triggered by Day 9: post-dentist comfort-food urge that Justin successfully resisted, then volunteered the disclosure plus stated readiness to design the protocol. Triggers identified: exhaustion, financial stress, physical/emotional discomfort.

The protocol's design respects the principle we set at intake: imposed protocols don't fire when the moment comes. So the structure was drafted from Justin's own articulated backup plan ("if the craving was really bad, I would have reached for the cottage cheese and waited a while before ordering a pizza"). Coach systematized; Justin owns it.

Three-step cascade: (1) name the urge, (2) primer + 20 min delay, (3) controlled indulgence with damage-control if step 2 doesn't catch it. Plus exhaustion-specific and financial-stress-specific variants.

Will be refined each time it fires (logged in journal entries).

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

### 2026-06-16 — Acceleration phase (Justin-initiated, Day 57)

Justin asked to **accelerate weight loss** by both tightening adherence and evolving the plan, after noticing the trailing line had been flat ~238 for ~2 weeks (clean weekday lows at 236 erased by weekend bounces). He brought six ideas; all adopted.

**1. Alcohol — the keystone change (his "biggest lever").** New policy (in `weekly-template.md`): **social-only** (no solo/ambient drinking while cooking, smoking, hanging), **target 1×/wk / hard cap 2×/wk**, **≤3 drinks per occasion**. Friday lunch right-sized 2–4 → ≤3. Rationale: last weekend ~1,900–2,500 alcohol calories ≈ the exact surplus erasing the weekday deficit; plus ethanol halts fat oxidation, fragments REM (his sleep slippage), and drives next-day grazing. This is the plateau-breaker. Reverses the long-standing "alcohol untouched" stance — and Justin initiated it, which is why the timing is right.

**2. Check-in cadence + breadth.** Back to **~3×/day** for mindfulness; **more verbose/engaged** than the old one-obs-one-suggestion floor; **rotating health probes** (hydration, sleep, energy, joints, NEAT, stress, cravings, caffeine, alcohol) since hydration + sleep drifted once we stopped asking. Occasional **DEEP-TRACK** re-baseline days. Codified in charter `CLAUDE.md`.

**3. Exercise variety.** Occasional joint-safe swaps to prevent rut + work new muscles — **always with form cues + a demo link** so Justin never has to research form. Pool stays inside disc/knee guardrails (no loaded forward flexion; core = anti-extension/rotation/lateral-flexion only).

**4. Outlive "why."** Weave Attia-aligned mechanism in ~2×/wk (Zone 2 = his elliptical, VO2 max, muscle-as-organ-of-longevity, stability, protein/sarcopenia). Justin reading it cover-to-cover, done ~late June.

**5. New tool — `justin/checkin_variety.py`.** Built to handle the randomness above (LLM randomness is weak). Deterministic per date; picks the day's probes, deep-track flag, optional exercise swap (with cues + YouTube demo link), and "why" thread. `--exercises` dumps the swap library. Run at check-in start.

**6. Push anchors + engage more.** Adopted — be willing to push on social anchors when there's real opportunity (the alcohol policy is the first instance), and ask Justin questions rather than only responding.

Also locked this session: **elliptical duration is now a floor not a cap** (extend toward 25–30 min when time allows — it's Zone 2 base; don't let it "earn" a bigger lunch), and the **mobility block moved to between strength and the elliptical** so the post-cardio fog stops eating the stretch.

### 2026-05-31 — Third formal 2-week review (Day 41)

**Numbers:**
- 7-day trailing avg: **238.2 lb** (calendar window, n=3: 5/27 239.3, 5/28 236.7, 5/31 238.6). Down from 239.7 at the 5/17 review — **−1.5 lb on the trailing line in 14 days, through a 4-day camping trip.**
- Total off baseline (250.0 home scale, Day 1): **−11.8 lb**
- Best daily: 236.7 lb (Thu 5/28 — new low)
- Pace: ~0.75 lb/wk this window — right at the 1 lb/wk target and notable for holding *through* the trip. The camping bump printed (239.3 on 5/27) and resolved on schedule, exactly as pre-framed.

**Major patterns this window:**

1. **Camping trip absorbed cleanly — the framework's central weight call paid off.** "Don't react to the daily bump; the trailing line resolves it" played out precisely: 241.6 midday off-protocol read on re-entry (excluded), 239.3 first clean morning (bump visible), 236.7 new daily + trailing low on 5/28 as the bump cleared. No vacation-hangover drift; first workout back was a full on-template session.

2. **Weight-reporting methodology unified across all three surfaces (5/28).** Discovered during the review that the coach check-ins, the `daily-update` skill, and `dashboard/build.py` were computing the trailing average three different ways — and the off-protocol 5/26 midday read (241.6) was inflating two of them. Fixed: **morning-only (drop reads ≥ noon), 7-day calendar window, same-morning multiples (2→avg, 3+→discard outlier).** All three surfaces now produce one number. Journal gap (5/21, 5/26, 5/27) backfilled from the conversation record; camping days 5/22–5/25 intentionally left blank.

3. **Self-directed band progression (5/28).** Justin added a band to the row/press work unprompted — "a push but still doable," clean form. Read his own readiness and progressed without being told. Maturity marker; the program is becoming his.

4. **Real-world trap navigation muscle is working in the wild.** Three documented this window: pretzel self-catch during dinner prep (5/27 — named the trigger, stopped, put the bag away); recital-day snack booth avoided + greek yogurt/caesar pre-load to control pizza slices (5/30); Friday social lunch self-regulated with a light protein dinner on the back end (5/29), unprompted. The comfort-food/environment-trap awareness is now reflexive, not coached.

**Justin's open feedback / insights this review:**

- **Waist measurement is technique-fragile** (Justin's flag): "there's a lot of variability depending on where I place the tape and how much breath I'm holding — I could probably game it several inches." Sharp self-observation that a once-weekly read can't separate signal from technique noise. Drove the protocol overhaul below.
- **KB squat progression:** open to either more reps or a heavier bell — deferred the method choice to the coach.
- **AM walk:** habit not yet formed; will work on it this week. No structural change — the lever is morning sunlight before noon, not the exact slot.

**Decisions / additions out of this review:**

KEEP (no change): primer, cottage cheese default, apple/fruit dessert, 8pm water cutoff, Mon–Thu workout split, weekly template, family anchors, Friday flex pattern, comfort-food protocol, Phase 1 stretching, minimum-effective-dose fallback, hydration anchors, dead bug in Mon core slot.

MODIFY:
- **KB squat progression flips from rep-driven to load-driven** — reverses the 5/17 DEFER on the KB upgrade. **35 lb KB ordered (arrives Wed 6/3)** — chose 35 over 30 for headroom (skips a near-term second purchase; the goblet limiter is grip/upper-back, not legs, so the big jump is safe). Bridge: Mon 6/1 stays 3×12 @ 20 lb; from Thu 6/4 on, **enter at 3×6–8 @ 35 lb → double-progress to 3×12** before adding load. Rationale: heavier load preserves lean mass better than reps in a deficit; goblet hold stays upright (joint-safe). Logged in `weekly-template.md`.
- **Band resistance baseline bumped** — the added band (5/28, clean form) formalized as the new baseline on row/press work.
- **Waist protocol overhauled** (see `weekly-template.md`): landmark moved to **top edge of navel** (single repeatable point > re-finding two bony landmarks); **2-week daily calibration sprint 6/1–6/14**, AM fasted; **log all 2–3 reads + the spread** (spread is the consistency metric), trend off the trailing average; mirror to keep tape level; then back off to 2–3×/week or weekly once spread is tight. `justin/waist.csv` created. The two pre-overhaul reads (5/17 ≈ 47.0, 5/31 = 47.5) are logged but flagged **not trend-comparable** (different landmark/cadence/technique).

NEW:
- **Weight-reporting methodology formalized** across coach + skill + dashboard (morning-only, 7-day calendar window, multiples rule). The off-protocol read class is now structurally excluded going forward.

HOLD / DEFER:
- **Family-history sweep** — held again per Justin (not the right beat this week). Stays on the docket for a natural opening in a coming check-in; not auto-triggered.
- **AM walk** — no structural change; Justin habituating this week.

EXPLORE / FILE:
- **Pan-seared salmon recipe** still unsaved — capture next time it's cooked.

**Next formal review: Sunday 2026-06-14** (also the waist calibration-sprint end date — they line up).

### 2026-05-17 — Second formal 2-week review (Day 27)

**Numbers:**
- 7-day trailing avg: **239.7 lb** (down from 242.9 at 5/4 review — −3.2 lb on trailing line in 13 days)
- Total off baseline (250.0 home scale, Day 1): **−10.3 lb**
- Best daily: 238.2 lb (Fri 5/15)
- **First sub-240 on the trailing line** since program start
- Pace: ~1.6 lb/wk, slightly above the 1 lb/wk target. Justin explicitly happy with this rate as long as it remains sustainable; "everything feels very sustainable."

**Major patterns this window:**

1. **Plate-composition flex is now a real skill.** 5 documented self-modifications within meals (lemon-not-butter on Mother's Day lobster; 100-cal bounded almond pack instead of prep-time grazing 5/12; 10 oz cottage cheese big primer for late 1:30 lunch 5/13; spaghetti pivot to meatball-forward / small pasta / no bread / green beans 5/15; controlled fajita night with 2 tortillas 5/16). Pattern: template provides the slot, Justin reshapes the plate based on the day. Opposite of the white-knuckle pattern.

2. **Sleep — n=1 structural finding + intervention in motion.** Mattress rotation experiment 5/14 flipped Justin's and Larissa's sleep in opposite directions on the same night. Justin: best sleep he can remember, zero morning back pain (he normally has mild low-back AM soreness — disc-injury-history-relevant). Larissa: tossed all night. Conclusion: mattress is worn. Mattress shopping initiated; new mattress acquisition expected over 5/16–5/17 weekend. Sleep lever shifts from behavioral (bedtime hit?) to structural (sleep quality + morning soreness).

3. **Hydration tightening (user-initiated, 5/14).** Justin flagged hydration off; coach + Justin built anchor-based plan (5 fixed pours tied to existing events — 12 oz on rising, glass with primer, glass with lunch, glass at start of afternoon work block, glass with dinner). ~75–80 oz with zero counting. Coach surfaces hydration at check-ins periodically per Justin's request.

4. **Recipe rotation hit target (5 saved).** Greek lemon chicken sheet pan, sheet-pan chicken thighs, Italian beef meatballs, crockpot white chicken chili, shrimp stir-fry. Chili already v1-iterated (bump solids next time). Recipes are living documents.

5. **Household architecture cleanly operational.** Folder restructure stable since 5/9; cross-session shared-notes channel load-tested across multiple round-trips; privacy rule honored.

**Justin's open feedback / insights this review:**

- **Food-noise reduction observation (Day 27).** Justin reports significant reduction in food-noise — the pre-program pattern of thinking about/fantasizing about pizza or fried food and struggling to resist the pantry is "gone." Asked if he's getting GLP-1-like benefits without the drug. Confirmed: yes, mechanistically real. Endogenous GLP-1 from primer (protein + fat) + sustained IF reducing baseline ghrelin + reward-stacked foods removed from frequent rotation reducing dopaminergic salience + template removing decision moments. He's getting a meaningful subset of GLP-1 effect via compounding behavioral mechanisms. The advantage over pharmacological GLP-1: doesn't reverse on stopping (because the behaviors *are* the program). This is the strongest sustainability argument identified so far. Logged in profile.md "What's working."
- Family: daughters enjoy the variety, miss some comfort foods (pizza, lasagne) but pushback isn't strong. Justin himself doesn't miss them. Open option: occasional comfort-food family meal every 2–3 weeks with Friday-flex applied to Justin's plate (parallel portions or restructured plate).
- AM walk addition (see below) — Justin's idea to add a 10-min AM something.

**Decisions / additions out of this review:**

KEEP (no change): primer, cottage cheese default, apple/fruit dessert, 8pm water cutoff, Mon–Thu workout split, weekly template, family anchors, Friday flex pattern, comfort-food protocol (still hasn't fired in anger — file as floor, not active tool), Phase 1 stretching, minimum-effective-dose workout fallback.

MODIFY (already in motion or now formalized):
- **Hydration anchor plan** formalized (5 fixed pours, yes/no reporting, coach surfaces periodically).
- **Mon workout gets dead bug 3×8/side** (locked for 5/18, parity with Tue/Thu) + rotation note for later weeks (bird dog, Pallof variations, hollow holds — all disc-friendly).
- **Standard warmup formalized** in `weekly-template.md` (band pull-aparts 2×15, arm circles, BW squats ×10 before every session).
- **Sleep tracking emphasis shifts** from "bedtime hit?" to "sleep quality + morning back pain" while the new mattress lands.

NEW:
- **AM 10-min walk slot.** ~First 30 min after waking, weather permitting. Primary lever: morning sunlight exposure (single biggest circadian-rhythm regulator). Stacks with the new mattress investment. Stretching as bad-weather fallback. Logged in `weekly-template.md`.
- **Phase 2 goal framing.** 220 is the current goal but not necessarily the final goal. At 220: celebrate the milestone, shift to maintenance for 3–4 weeks (let body settle out of deficit), then reassess. Phase 2 might target 210 or 200 *or* maintenance — decision driven by composition, energy, lifts, felt experience, and waist circumference (the one measurement worth adding at the 220 checkpoint). Don't slow approaching 220, but explicitly switch to maintenance on arrival rather than rolling momentum past it.
- **Plate-composition flex skill named.** This is now an established behavior, not a one-off win.
- **Bounded snack tool** (100-cal pre-portioned pack) added as a third tool for prep-time hunger.
- **Recipe-as-living-document** pattern named.

EXPLORE / FILE:
- **Family-history sweep** (proposed via shared-notes 2026-05-18). Justin's intake captured only single-line family history (mother's wheat sensitivity / joint connection). Schedule 10–15 min of directed questions at a coming check-in; results land in `profile.md` under new Family history section. Cardiovascular, bone density, autoimmune, metabolic, mental health, cancer — all in scope.
- **Mattress effect** — once new mattress lands, watch for downstream effects on afternoon snack intensity, stress reactivity, workout perception.
- **Memorial Day weekend camping (5/22–5/25)** — Justin pre-framed correctly: maintain IF + primer + protein-forward where reasonable; intentional relaxation elsewhere; accept a few days of setback. Practical adds: protein-portable primer options (cottage cheese cups, HB eggs, jerky), hydration anchor with extra emphasis (alcohol + sun + camping-food sodium), protein-with-each-meal is the one not to abandon, post-trip Tuesday just resume the template (no make-up restriction).
- **Wheat sensitivity hypothesis** — still single data point + multiple confounders. No new correlation this window. Continue to file, don't chase.
- **Occasional extended fasts (OMAD 1–2×/week for autophagy)** — discussed Day 27. Decision: **defer, revisit at maintenance / Phase 2 decision point.** Reasons: human evidence for "16-hour autophagy trigger" weaker than podcast discourse suggests; Justin already getting baseline autophagy at 17:7; marginal autophagy gains uncertain; concrete costs (protein/muscle protection during deficit; workout fueling; system complexity vs. template-eater principle). Not contraindicated, just not the right risk/reward in deficit phase. Revisit at 220.

DEFER:
- 35 lb KB upgrade (bands still have headroom).
- Saturday alcohol dose experiment (trend on pace; no trigger to touch).
- Calorie counting (still not needed).

ADD (revised in-review per Justin's push 2026-05-17):
- **Waist circumference, weekly Saturday AM fasted.** Reversed from initial DEFER — Justin's case for trend-building beats waiting for a single 220-checkpoint snapshot. Visceral-fat proxy; can decouple from scale weight (recomposition signal). Logged in journal on measurement days; will spin up a CSV once we have ~4 data points. First measurement: Justin's choice of today (baseline before camping) or Sat 5/30 (clean start post-trip).

**Next formal review: Sunday 2026-05-31.** (Note: 5/22–5/25 camping weekend falls in the window. Expect a noisy trailing-line bump 5/25–5/29 that resolves by next review.)

### 2026-05-04 — First formal 2-week review (14 days in)

**Numbers:**
- Home scale start: 250.0 lb
- 7-day trailing avg: 242.9 lb (down 4.6 lb on the trailing line over 12 days of Withings data)
- Pace faster than 1 lb/wk target; week-1 was glycogen+water dominant. Expect slope to find a more sustainable level over weeks 3–4.

**Major structural wins (Justin's words and observations):**
- Afternoon snack appetite "completely disappeared" — confirmed structural, not white-knuckle.
- GI improvements: less night-time gas/bloating; one consistent AM poop vs prior 2–3/day variable; clothes fitting noticeably better. All connected — gut + insulin + visceral fat all responding.
- Estimated ~1000 cal/day swing from prior baseline (afternoon drift + pre-prep grazing + oversized lunches removed; primer + extra protein added; net deficit substantial).
- Hard-day adherence proven 3 separate times (yard work day, patio build day, post-dentist comfort food urge).
- Comfort-food protocol designed Day 9 from Justin's own articulated structure.
- Wife stakeholder loop closed: chickpea request → showed up in salad → "really appreciated."
- Sleep improving: 11:15 target hit ~50%+ weeknights, midnight-wakes resolved with 8pm water cutoff.

**Justin's open feedback:**
- Very little friction; feels great about all of it.
- IF + primer combo works because both are decision-free.
- Coach-supported meal planning is "significant de-stressor."
- Wants more "why" / science alongside the "what" going forward.
- Workout schedule unpredictable — needs minimum-effective-dose protocol for tight-work days.

**Decisions / additions out of this review:**

KEEP (no change): primer, cottage cheese default, apple/fruit dessert, 8pm water cutoff, Mon–Thu workout split, weekly template, family anchors, Friday flex pattern.

MODIFY (small):
- Push protein consistently to 150–180 g/day target by eating full dinner protein, adding HB egg to lunches, etc.
- Plant-forward dinners ≥1/week (chickpeas in Thursday salad was v1).
- Add **post-workout stretching protocol** (Phase 1: 5 stretches, ~5–7 min, Mon/Tue/Thu). Phase 2 (weeks 3–4): Sat/Sun mobility session. Phase 3 later: one weekly gentle yoga.
- Add **minimum-effective-dose workout fallback** (20 min something) for unpredictable work days.

EXPLORE / FILE:
- Wheat sensitivity hypothesis (still single data point + confounders; await second correlation).
- Comfort-food protocol stress-testing (will know when it fires in anger).
- Recipe rotation expansion (target: 5 saved recipes by next review).

DEFER:
- 35 lb KB upgrade (bands not yet maxed).
- Saturday alcohol dose experiment (revisit only if trend stalls).
- Calorie counting (not needed; counterproductive).

NEW:
- **Diet soda** declared as a managed craving (not active habit). Coach offered sparkling water swap + restaurant default (soda water + lime).
- **Hydration:** Justin self-aware that natural thirst is low. Voluntary tracking continues; environmental cues (desk water bottle, water-before-coffee anchor).
- **Coaching style addition:** include brief mechanism ("the why") with recommendations going forward. Not constant; at decision points.
- **Avocado position:** good food, not magic; fine as topping (¼–½ avo on a salad/wrap), not as snack-as-meal substitute (240 cal, 3g protein — wrong density for the goal).

**Next review: Sunday 2026-05-18** (2 more weeks).

### 2026-04-25 — Mid-week informal review (5 days in)

- Weight trend (Withings only): 247.5 → 246.1 → 244.6 lb (3 data points; noise-level, but direction is right). Home-scale start: 250.0.
- Adherence: high. Primer hit every day; one cookie incident (small, dismissed); Mexican lunch executed clean.
- Sleep: improving. Best night: Thu 11:00 lights-out clean. Friday: midnight (dance comp, family obligation > rule).
- Coach added: protein target 150–180 g/day; pivoted to weekly template; codified weigh-in / journaling rules; added wife as stakeholder; added air fryer + crockpot to equipment-aware planning.
- Open: Justin's wife's specific goals if she chooses to share; first plant-forward dinner to land in week 2; experiment with bigger primer or protein-shake top-up to close the protein gap.
