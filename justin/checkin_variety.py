#!/usr/bin/env python3
"""Check-in variety helper for Justin's coaching sessions.

Removes coach repetitiveness (and the LLM's weak randomness) by selecting,
*deterministically per calendar date*, what to vary in a given day's check-in:

  - which 2-3 HEALTH FACTORS to probe (rotating pool)
  - whether today is a DEEP-TRACK day (detailed re-baseline of one factor)
  - whether to suggest an EXERCISE SWAP, and which (joint-safe pool only)
  - whether to weave in an Outlive-style "WHY" thread

Deterministic per date means a given day always yields the same brief, so the
coach can re-run it any time that day and get a stable result. Pass --date to
preview another day; --exercises to dump the full swap library.

Pure standard library. Run from project root:  python justin/checkin_variety.py
"""

import argparse
import datetime as dt
import hashlib
import random

# --- Health-factor probe pool -------------------------------------------------
# These drifted once we stopped asking (hydration + sleep, ~June). Rotating a
# couple per day keeps mindfulness up without a daily 10-question interrogation.
HEALTH_FACTORS = {
    "hydration": "Hydration — hitting the 5 anchor pours? Any afternoon dip?",
    "sleep_time": "Sleep — lights-out time last night + roughly how many hours?",
    "sleep_quality": "Sleep quality — wake-ups? morning back soreness? feel rested?",
    "energy": "Energy / mood today (1-5)?",
    "joints": "Joints — knees / feet / PsA: anything talking today?",
    "neat": "NEAT — on your feet much today, or a heavy desk day?",
    "stress": "Stress (1-5)? Anything weighing on you?",
    "cravings": "Food noise / cravings — any, and roughly what time?",
    "caffeine": "Caffeine — when was the last cup? (protecting 11:15 lights-out)",
    "alcohol": "Alcohol — any today? was it social? (social-only, <=3, 1-2x/wk)",
}

# Factors that support a detailed re-baseline day.
DEEP_TRACK = {
    "hydration": (
        "DEEP-TRACK HYDRATION today — log every drink (oz) + timing through the "
        "day so we can re-baseline against the ~80 oz aim and spot the weak slot."
    ),
    "sleep": (
        "DEEP-TRACK SLEEP today — lights-out, wake time, # of awakenings, AM "
        "back/soreness, and restedness (1-5). Rebuilds the sleep baseline."
    ),
}

# --- Outlive-style "why" threads (weave in ~twice a week) ---------------------
WHY_TOPICS = {
    "zone2": "Zone 2 — your conversational-pace elliptical IS Zone 2. Builds "
             "mitochondrial density + fat-oxidation capacity (Attia's aerobic "
             "base) — the exact engine alcohol blunts. Why we're extending it.",
    "vo2max": "VO2 max — the strongest single predictor of all-cause mortality "
              "in Attia's framing. The Zone 2 base now is what lets us add a "
              "little higher-intensity later to raise the ceiling.",
    "muscle": "Muscle = the 'organ of longevity.' Lean mass is your reserve for "
              "the back half of life (Attia's Centenarian Decathlon). It's why we "
              "load-progress the KB in a deficit instead of just adding reps.",
    "protein": "Protein & sarcopenia — at 49 you have anabolic resistance, so you "
               "need MORE protein to defend muscle, not less. That's the whole "
               "case for the 150-180 g target while cutting.",
    "stability": "Stability — Attia's overlooked fourth pillar. Dead bug, Pallof, "
                 "and carries build the brace that protects your disc-history "
                 "back. Boring-looking, high-leverage.",
    "sleep_metab": "Sleep & metabolism — short/fragmented sleep raises ghrelin, "
                   "drops leptin, and worsens insulin sensitivity. Poor sleep "
                   "directly sabotages the deficit by ramping next-day hunger.",
    "alcohol": "Alcohol — near-zero health upside: it halts fat oxidation while "
               "it's metabolized and fragments REM sleep. Calories AND a metabolic "
               "timeout. Your current single biggest lever.",
    "visceral": "Visceral fat — the metabolically dangerous fat sits around the "
                "organs and tracks with waist circumference better than scale "
                "weight. That's why we measure the waist, not just weigh in.",
}

# --- Joint-safe exercise swap library ----------------------------------------
# HARD CONSTRAINT: no loaded forward flexion (disc-injury history). Core is
# anti-extension / anti-rotation / anti-lateral-flexion ONLY — no sit-ups,
# crunches, or weighted twists. Knee/foot items carry a check note.
# "demo" links are YouTube SEARCH urls (always valid; land on a form demo).
def _yt(q):
    return "https://www.youtube.com/results?search_query=" + q.replace(" ", "+")


EXERCISES = [
    # ---- WARMUP (mix in for ONE of the 3 standards: band pull-apart,
    #      arm circles, bodyweight squat). General prep, not a stimulus. ----
    {"slot": "warmup", "name": "Cat-cow",
     "cues": "On hands+knees, alternate arching (look up) and rounding (tuck "
             "chin) the spine with your breath. 8-10 slow reps.",
     "why": "Gentle spinal mobility — primes the back before any loading.",
     "joint": "Disc-friendly; stay in a comfortable, controlled range.",
     "demo": _yt("cat cow exercise form")},
    {"slot": "warmup", "name": "Leg swings",
     "cues": "Hold something for balance; swing one leg front-to-back x10, then "
             "side-to-side x10. Controlled, not ballistic. Switch legs.",
     "why": "Dynamic hip mobility before squats/split squats.",
     "joint": "Easy on the knees; keep the swing controlled.",
     "demo": _yt("leg swings warm up form")},
    {"slot": "warmup", "name": "Band shoulder pass-through",
     "cues": "Wide grip on the band, sweep it from in front, overhead, to behind "
             "you and back. Slow. 8-10. Widen grip if tight.",
     "why": "Opens shoulders + chest for pressing and counters desk posture.",
     "joint": "Shoulder mobility; never force the range.",
     "demo": _yt("band shoulder pass through dislocate form")},
    {"slot": "warmup", "name": "Scapular pushups",
     "cues": "Top of a pushup, arms straight the whole time — pinch shoulder "
             "blades together, then push the floor away to spread them. 10 reps.",
     "why": "Wakes up the serratus/scaps before pressing — better, safer pushups.",
     "joint": "Shoulder-friendly; no elbow bend.",
     "demo": _yt("scapular pushups form")},
    {"slot": "warmup", "name": "90/90 hip switches",
     "cues": "Sit with both knees bent ~90deg, one in front one to the side; "
             "rotate both knees to the other side. 8/side, controlled.",
     "why": "Hip rotational mobility — opens the hips for deeper, cleaner squats.",
     "joint": "Gentle; don't force the range.",
     "demo": _yt("90 90 hip switch mobility form")},

    # ---- LOWER (sub for KB goblet squat) ----
    {"slot": "lower", "name": "Tempo goblet squat (3s descent)",
     "cues": "Same KB goblet hold; lower for a slow 3-count, pause 1s at the "
             "bottom, drive up normally. Chest tall, knees track over toes.",
     "why": "More time-under-tension at the same 35 lb — extra stimulus without "
            "a heavier bell.",
     "joint": "Knee-friendly; the slow eccentric is actually easier on the joint "
              "than bouncing.", "demo": _yt("tempo goblet squat form")},
    {"slot": "lower", "name": "KB split squat (static lunge)",
     "cues": "Feet split front/back, KB in goblet hold. Drop the back knee "
             "straight down, torso upright, front shin near-vertical. 3x8/leg.",
     "why": "Unilateral — exposes and fixes left/right imbalance; big glute/quad "
            "recruitment.",
     "joint": "KNEE CHECK: keep front knee tracking over the foot; shorten range "
              "if the knee complains. Stop if sharp pain.",
     "demo": _yt("dumbbell split squat form")},
    {"slot": "lower", "name": "Single-leg glute bridge",
     "cues": "On your back, one foot planted, other leg extended. Drive through "
             "the heel, squeeze the glute at the top, don't arch the low back. "
             "3x10/leg.",
     "why": "Posterior-chain + glute strength with zero spinal load — pairs well "
            "after squats.",
     "joint": "Very back-friendly; no flexion under load.",
     "demo": _yt("single leg glute bridge form")},
    {"slot": "lower", "name": "Wall sit (isometric)",
     "cues": "Back flat on a wall, slide to thighs-parallel, hold. 3x30-45s. "
             "Add the KB on the lap to progress.",
     "why": "Pure quad isometric — joint-quiet way to accumulate leg work on a "
            "cranky-knee day.",
     "joint": "Gentle; reduce depth if knees object.", "demo": _yt("wall sit exercise form")},

    # ---- PUSH (sub for pushups / band chest press) ----
    {"slot": "push", "name": "Tempo pushup (3s descent)",
     "cues": "Standard pushup, lower for a slow 3-count, press up normally. Body "
             "in one line, elbows ~45deg (not flared to 90).",
     "why": "Doubles the chest/triceps stimulus at bodyweight — progress without "
            "adding load.",
     "joint": "Shoulder-friendly at 45deg elbows.", "demo": _yt("tempo pushup form")},
    {"slot": "push", "name": "Band overhead press",
     "cues": "Stand on the band, press handles from shoulders to overhead, ribs "
             "down (don't arch back), full lockout. 3x10-12.",
     "why": "Vertical press — hits shoulders/triceps the horizontal pushup "
            "misses; rounds out pressing.",
     "joint": "Keep ribs down to protect the low back; stop if shoulder pinches.",
     "demo": _yt("resistance band overhead press form")},
    {"slot": "push", "name": "Pike pushup",
     "cues": "Hips up in an inverted-V, hands shoulder-width, lower the crown of "
             "your head toward the floor, press back up. 3x8.",
     "why": "Bodyweight shoulder builder — bridge toward eventual handstand-type "
            "pressing.",
     "joint": "SHOULDER CHECK: keep range comfortable; skip if it impinges.",
     "demo": _yt("pike pushup form")},

    # ---- PULL (sub for band row / lat pulldown) ----
    {"slot": "pull", "name": "Band face pull",
     "cues": "Anchor band at face height, pull toward your forehead with elbows "
             "high, thumbs back at the end. 3x15. Slow return.",
     "why": "Rear delts + mid-traps — the #1 posture antidote for a WFH desk "
            "neck/shoulders.",
     "joint": "Very joint-friendly; light load, high reps.",
     "demo": _yt("resistance band face pull form")},
    {"slot": "pull", "name": "Band single-arm row",
     "cues": "Anchor low/mid, one arm at a time, row to the hip, squeeze the "
             "shoulder blade, control the return. 3x10-12/arm.",
     "why": "Unilateral back work — fixes side-to-side pulling imbalance the "
            "two-arm row hides.",
     "joint": "Back-friendly; keep torso steady, don't twist.",
     "demo": _yt("single arm resistance band row form")},
    {"slot": "pull", "name": "Band straight-arm pulldown",
     "cues": "Anchor band high, arms nearly straight, pull the handles down to "
             "your thighs using the lats, slow return. 3x12-15.",
     "why": "Isolates the lats without biceps taking over — different feel from "
            "rows.",
     "joint": "Joint-quiet.", "demo": _yt("straight arm band pulldown form")},

    # ---- CORE (anti-extension / anti-rotation / anti-lateral-flexion ONLY) ----
    {"slot": "core", "name": "Suitcase carry (single KB)",
     "cues": "Hold the 35 lb KB in ONE hand, stand tall, walk 30-40 steps "
             "without leaning. Switch sides. 3 trips/side.",
     "why": "Anti-lateral-flexion core + grip + traps — huge real-world carryover, "
            "uses the bell you already have.",
     "joint": "Excellent for disc history — teaches the brace under load with no "
              "spinal flexion.", "demo": _yt("suitcase carry exercise form")},
    {"slot": "core", "name": "Bird dog",
     "cues": "On hands+knees, extend opposite arm + leg, hold 2s, keep hips level "
             "(don't rotate). 3x8/side. Slow and controlled.",
     "why": "Anti-rotation + spinal stability — the McGill staple for backs.",
     "joint": "Gold-standard disc-safe core.", "demo": _yt("bird dog exercise form")},
    {"slot": "core", "name": "Side plank",
     "cues": "On forearm, body in a straight line, hips stacked and lifted. "
             "3x20-40s/side. Drop to knees to regress.",
     "why": "Anti-lateral-flexion — builds the obliques/QL that guard the spine.",
     "joint": "Disc-safe; no flexion.", "demo": _yt("side plank form")},
    {"slot": "core", "name": "Front plank (long-lever)",
     "cues": "Forearm plank, squeeze glutes + brace abs, slide elbows slightly "
             "forward to make it harder. 3x30-45s. No sagging hips.",
     "why": "Anti-extension brace — same family as the dead bug.",
     "joint": "Disc-safe.", "demo": _yt("forearm plank form")},
]

# Weekday -> workout slots available for a swap suggestion (Mon=0 .. Sun=6).
SESSION_SLOTS = {
    0: ["lower", "push", "core"],   # Mon: Lower + Push + Core
    1: ["pull", "core"],            # Tue: Upper Pull + Core
    2: [],                          # Wed: cardio/mobility — no swap
    3: ["lower", "push", "pull", "core"],  # Thu: Full body
    4: [],                          # Fri: rest
    5: [],                          # Sat: active recovery
    6: [],                          # Sun: active recovery
}

SLOT_LABEL = {"lower": "LOWER (KB squat)", "push": "PUSH", "pull": "PULL",
              "core": "CORE", "warmup": "WARMUP"}

# Tunable frequencies (probability per day).
P_DEEP_TRACK = 1 / 7      # ~once a week
P_WHY = 2 / 7             # ~twice a week
P_EXERCISE_SWAP = 0.33    # ~1 in 3 workout days
P_WARMUP_SWAP = 0.25      # ~1 in 4 workout days (warmup stays mostly standard)


def _rng_for(date):
    seed = int(hashlib.sha256(date.isoformat().encode()).hexdigest(), 16) % (2**32)
    return random.Random(seed)


def build_brief(date):
    rng = _rng_for(date)
    out = []
    weekday = date.weekday()
    out.append(f"==== Coach variety brief — {date.isoformat()} "
               f"({date.strftime('%A')}) ====")

    # Health probes: 2-3 rotating factors.
    n = rng.choice([2, 2, 3])
    keys = rng.sample(list(HEALTH_FACTORS), n)
    out.append("\nHEALTH PROBES (work these into the check-in):")
    for k in keys:
        out.append(f"  - {HEALTH_FACTORS[k]}")

    # Deep-track day?
    if rng.random() < P_DEEP_TRACK:
        which = rng.choice(list(DEEP_TRACK))
        out.append("\n[DEEP-TRACK DAY]")
        out.append(f"  - {DEEP_TRACK[which]}")

    # Exercise swap (workout days only).
    slots = SESSION_SLOTS.get(weekday, [])
    if slots and rng.random() < P_EXERCISE_SWAP:
        slot = rng.choice(slots)
        pool = [e for e in EXERCISES if e["slot"] == slot]
        ex = rng.choice(pool)
        out.append(f"\nEXERCISE SWAP (optional — offer it for the {SLOT_LABEL[slot]} slot):")
        out.append(f"  {ex['name']}")
        out.append(f"    What/cues: {ex['cues']}")
        out.append(f"    Why:       {ex['why']}")
        out.append(f"    Joint:     {ex['joint']}")
        out.append(f"    Demo:      {ex['demo']}")

    # Warmup tweak (workout days only; stays mostly standard).
    if slots and rng.random() < P_WARMUP_SWAP:
        ex = rng.choice([e for e in EXERCISES if e["slot"] == "warmup"])
        out.append("\nWARMUP TWEAK (optional — mix in for ONE of the 3 standards):")
        out.append(f"  {ex['name']}")
        out.append(f"    What/cues: {ex['cues']}")
        out.append(f"    Why:       {ex['why']}")
        out.append(f"    Demo:      {ex['demo']}")

    # "Why" thread.
    if rng.random() < P_WHY:
        topic = rng.choice(list(WHY_TOPICS))
        out.append("\n\"WHY\" THREAD (weave in once, Outlive-style):")
        out.append(f"  - {WHY_TOPICS[topic]}")

    return "\n".join(out)


def list_exercises():
    out = ["==== Joint-safe exercise swap library ===="]
    for slot in ["warmup", "lower", "push", "pull", "core"]:
        out.append(f"\n--- {SLOT_LABEL[slot]} ---")
        for e in [x for x in EXERCISES if x["slot"] == slot]:
            out.append(f"  {e['name']}")
            out.append(f"    {e['cues']}")
            out.append(f"    Demo: {e['demo']}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Daily check-in variety brief.")
    ap.add_argument("--date", help="YYYY-MM-DD (default: today)")
    ap.add_argument("--exercises", action="store_true",
                    help="print the full exercise swap library and exit")
    args = ap.parse_args()

    if args.exercises:
        print(list_exercises())
        return

    date = (dt.date.fromisoformat(args.date) if args.date else dt.date.today())
    print(build_brief(date))


if __name__ == "__main__":
    main()
