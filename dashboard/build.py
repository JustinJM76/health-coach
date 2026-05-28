#!/usr/bin/env python3
"""Render light-themed coaching dashboards for Justin and Larissa.

Reads each principal's most-recent plan, weight history, the household meal plan, and the
reading list, then writes self-contained HTML pages to dashboard/<principal>.html.

Uses pyyaml for plan frontmatter and Chart.js + Marked.js from CDN for the weight chart and
markdown bodies. No build step, no Python markdown dependency.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = ROOT / "dashboard"
HOUSEHOLD_DIR = ROOT / "household"

PRINCIPALS = [
    {"key": "justin", "name": "Justin", "dir": ROOT / "justin"},
    {"key": "larissa", "name": "Larissa", "dir": ROOT / "larissa"},
]


def load_today_plan(principal_dir: Path) -> tuple[dict | None, str]:
    today = dt.date.today().isoformat()
    plan_path = principal_dir / "plans" / f"{today}.md"
    if not plan_path.exists():
        candidates = sorted((principal_dir / "plans").glob("*.md"))
        if not candidates:
            return None, ""
        plan_path = candidates[-1]
    text = plan_path.read_text()
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}
    body = parts[2].strip() if len(parts) > 2 else ""
    return frontmatter, body


def load_weight_history(measurements_csv: Path, days: int = 90) -> list[dict]:
    """Per-weigh-in points (raw); multiple per day collapsed by aggregate_daily."""
    if not measurements_csv.exists():
        return []
    cutoff = dt.date.today() - dt.timedelta(days=days)
    rows: list[dict] = []
    with measurements_csv.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            iso = row.get("date_iso") or ""
            kg = row.get("weight_kg") or ""
            if not iso or not kg:
                continue
            try:
                ts = dt.datetime.fromisoformat(iso)
                d = ts.date()
                lb = round(float(kg) * 2.20462, 1)
            except ValueError:
                continue
            if d < cutoff:
                continue
            # Morning weigh-ins only (protocol: morning, fasted, after coffee + BM).
            # Drop midday/evening step-ons (>= noon) — not valid trend data.
            if ts.hour >= 12:
                continue
            rows.append({"date": d.isoformat(), "weight_lb": lb})
    rows.sort(key=lambda r: r["date"])
    return rows


def aggregate_daily(weighins: list[dict]) -> list[dict]:
    """Multiple weigh-ins on the same day → mean."""
    by_date: dict[str, list[float]] = {}
    for r in weighins:
        by_date.setdefault(r["date"], []).append(r["weight_lb"])
    return [
        {"date": d, "weight_lb": round(sum(vs) / len(vs), 1)}
        for d, vs in sorted(by_date.items())
    ]


def rolling_average(daily: list[dict], window: int = 7) -> list[float | None]:
    """Trailing N-calendar-day mean per day; None until the window has at least 2 entries.

    Calendar-window (not entry-window): during multi-day gaps (e.g., travel) the window
    holds fewer points rather than reaching further back in time.
    """
    out: list[float | None] = []
    dates = [dt.date.fromisoformat(p["date"]) for p in daily]
    for i in range(len(daily)):
        lo = dates[i] - dt.timedelta(days=window - 1)
        recent = [daily[j]["weight_lb"] for j in range(i + 1) if dates[j] >= lo]
        if len(recent) < 2:
            out.append(None)
        else:
            out.append(round(sum(recent) / len(recent), 2))
    return out


def linear_trend(daily: list[dict]) -> list[float] | None:
    """Best-fit line projected across the series. Returns y-values aligned to daily."""
    n = len(daily)
    if n < 3:
        return None
    xs = list(range(n))
    ys = [p["weight_lb"] for p in daily]
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    den = sum((x - x_mean) ** 2 for x in xs)
    if den == 0:
        return None
    slope = num / den
    intercept = y_mean - slope * x_mean
    return [round(slope * x + intercept, 1) for x in xs]


GOAL_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:→|->|to)\s*(\d+(?:\.\d+)?)\s*lb", re.IGNORECASE)


def parse_goal_endpoints(plan: dict | None) -> tuple[float | None, float | None]:
    """Extract (start_lb, goal_lb) from any goal title like '250 → 220 lb'."""
    if not plan:
        return None, None
    for g in plan.get("goals") or []:
        if not isinstance(g, dict):
            continue
        title = g.get("title") or ""
        m = GOAL_RE.search(title)
        if m:
            return float(m.group(1)), float(m.group(2))
    return None, None


def read_or_empty(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def resolve_relative(principal_dir: Path, rel: str | None) -> Path | None:
    if not rel:
        return None
    p = (principal_dir / rel).resolve()
    try:
        p.relative_to(ROOT)
    except ValueError:
        return None
    return p if p.exists() else None


def collect_inline_files(principal_dir: Path, plan: dict) -> dict[str, str]:
    """For each meal/workout in the plan with a path, read the file content for inline embed."""
    out: dict[str, str] = {}
    if not plan:
        return out
    workout = plan.get("workout") or {}
    if isinstance(workout, dict):
        wp = resolve_relative(principal_dir, workout.get("details_path"))
        if wp:
            out[workout["details_path"]] = read_or_empty(wp)
    for meal in plan.get("meals") or []:
        if not isinstance(meal, dict):
            continue
        rp = resolve_relative(principal_dir, meal.get("recipe_path"))
        if rp:
            out[meal["recipe_path"]] = read_or_empty(rp)
    return out


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — coaching dashboard</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<style>
:root {{
  --bg: #fafaf7;
  --surface: #ffffff;
  --border: #e6e3da;
  --text: #1f2937;
  --muted: #6b7280;
  --accent: #0d9488;
  --accent-soft: #ccfbf1;
  --pop: #fb7185;
  --shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 4px 12px rgba(15, 23, 42, 0.04);
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}}
main {{ max-width: 880px; margin: 0 auto; padding: 24px 20px 64px; }}
header.hero {{
  background: linear-gradient(135deg, var(--accent) 0%, #14b8a6 100%);
  color: white;
  border-radius: 18px;
  padding: 28px 28px 26px;
  box-shadow: var(--shadow);
}}
header.hero .row {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 16px;
  flex-wrap: wrap;
}}
header.hero h1 {{
  margin: 0;
  font-size: 30px;
  letter-spacing: -0.01em;
}}
header.hero .date {{
  font-size: 14px;
  opacity: 0.9;
  font-variant-numeric: tabular-nums;
}}
header.hero blockquote {{
  margin: 16px 0 0;
  padding: 12px 16px;
  background: rgba(255,255,255,0.18);
  border-left: 4px solid var(--pop);
  border-radius: 8px;
  font-style: italic;
  font-size: 16px;
}}
section.card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px 24px;
  margin-top: 20px;
  box-shadow: var(--shadow);
}}
section.card h2 {{
  margin: 0 0 14px;
  font-size: 16px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--muted);
}}
.metric-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}}
.metric {{
  background: var(--accent-soft);
  border-radius: 10px;
  padding: 12px 14px;
}}
.metric .label {{
  font-size: 12px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}
.metric .value {{
  font-size: 22px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--accent);
}}
.metric .delta {{
  font-size: 13px;
  color: var(--muted);
}}
.metric .delta.down {{ color: #16a34a; }}
.metric .delta.up {{ color: #dc2626; }}
.goal {{ margin: 8px 0 0; }}
.goal-title {{ font-weight: 600; }}
.goal-status {{
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 999px;
  margin-left: 6px;
  background: var(--accent-soft);
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.goal-status.watch {{ background: #fef3c7; color: #b45309; }}
.goal-status.off-track {{ background: #fee2e2; color: #b91c1c; }}
.goal-status.tbd {{ background: #f3f4f6; color: var(--muted); }}
.plan-row {{
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-top: 1px solid var(--border);
}}
.plan-row:first-child {{ border-top: none; }}
.plan-row .icon {{ font-size: 20px; flex: 0 0 28px; }}
.plan-row .body {{ flex: 1; }}
.plan-row .label {{
  font-size: 11px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}
.plan-row .text {{ margin-top: 2px; }}
details.embed {{
  margin-top: 8px;
  background: var(--bg);
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 14px;
}}
details.embed > summary {{
  cursor: pointer;
  color: var(--accent);
  font-weight: 500;
  list-style: none;
}}
details.embed > summary::before {{ content: "▸ "; }}
details.embed[open] > summary::before {{ content: "▾ "; }}
details.embed .md {{ padding: 8px 4px 4px; }}
ul.tasks {{ list-style: none; padding-left: 0; margin: 0; }}
ul.tasks li {{
  padding: 6px 0 6px 26px;
  position: relative;
}}
ul.tasks li::before {{
  content: "✓";
  position: absolute;
  left: 4px;
  color: var(--accent);
  font-weight: 700;
}}
.coach-note {{
  margin-top: 14px;
  padding: 14px 16px;
  background: #fff7ed;
  border-left: 3px solid var(--pop);
  border-radius: 6px;
  font-size: 14px;
}}
.empty {{
  color: var(--muted);
  font-style: italic;
}}
.md h1, .md h2, .md h3 {{ margin-top: 14px; margin-bottom: 6px; }}
.md h1 {{ font-size: 18px; }}
.md h2 {{ font-size: 16px; }}
.md h3 {{ font-size: 14px; }}
.md ul, .md ol {{ padding-left: 24px; }}
.md p {{ margin: 6px 0; }}
.md a {{ color: var(--accent); }}
canvas#weightChart {{ width: 100% !important; height: 320px !important; }}
footer.tiny {{
  margin-top: 28px;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
}}
</style>
</head>
<body>
<main>
  <header class="hero">
    <div class="row">
      <h1>{name}</h1>
      <div class="date">{date_pretty}</div>
    </div>
    <blockquote>{motd_html}</blockquote>
  </header>

  <section class="card" id="progress">
    <h2>Progress &amp; goals</h2>
    {progress_html}
    {chart_html}
    {goals_html}
  </section>

  <section class="card" id="today">
    <h2>Today's plan</h2>
    {plan_html}
    {coach_note_html}
  </section>

  <section class="card" id="meal-plan">
    <h2>This week's meal plan</h2>
    <div class="md" data-md="meal_plan"></div>
  </section>

  <section class="card" id="reading">
    <h2>Reading list</h2>
    <div class="md" data-md="reading_list"></div>
  </section>

  <footer class="tiny">Generated {generated_at} · {principal_key}</footer>
</main>

<script id="payload" type="application/json">{payload_json}</script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
(function() {{
  const data = JSON.parse(document.getElementById('payload').textContent);

  // Render markdown placeholders.
  document.querySelectorAll('[data-md]').forEach(el => {{
    const key = el.dataset.md;
    const src = data[key] || '';
    el.innerHTML = src.trim() ? marked.parse(src) : '<p class="empty">(none)</p>';
  }});

  // Render inline-embed details bodies (recipes, workout details).
  document.querySelectorAll('[data-embed]').forEach(el => {{
    const key = el.dataset.embed;
    const src = (data.embeds && data.embeds[key]) || '';
    el.innerHTML = src.trim() ? marked.parse(src) : '<p class="empty">(file not found)</p>';
  }});

  // Weight chart — multiple overlaid datasets.
  const chartEl = document.getElementById('weightChart');
  const chart = data.chart || {{}};
  if (chartEl && chart.labels && chart.labels.length) {{
    const datasets = [];
    // Order matters: lower-z first.
    if (chart.daily && chart.daily.length) {{
      datasets.push({{
        label: 'Daily',
        data: chart.daily,
        borderColor: 'rgba(13, 148, 136, 0.35)',
        backgroundColor: 'rgba(13, 148, 136, 0.05)',
        borderWidth: 1,
        pointRadius: 1.5,
        pointBackgroundColor: 'rgba(13, 148, 136, 0.4)',
        tension: 0.15,
        fill: false,
        order: 4,
      }});
    }}
    if (chart.start_line && chart.start_line.length) {{
      datasets.push({{
        label: 'Start (' + chart.start_lb + ' lb)',
        data: chart.start_line,
        borderColor: '#9ca3af',
        borderDash: [4, 4],
        borderWidth: 1.5,
        pointRadius: 0,
        fill: false,
        order: 3,
      }});
    }}
    if (chart.goal_line && chart.goal_line.length) {{
      datasets.push({{
        label: 'Goal (' + chart.goal_lb + ' lb)',
        data: chart.goal_line,
        borderColor: '#fb7185',
        borderDash: [4, 4],
        borderWidth: 1.5,
        pointRadius: 0,
        fill: false,
        order: 3,
      }});
    }}
    if (chart.trend && chart.trend.length) {{
      datasets.push({{
        label: 'Trend',
        data: chart.trend,
        borderColor: '#0d9488',
        borderDash: [2, 4],
        borderWidth: 1.5,
        pointRadius: 0,
        fill: false,
        order: 2,
      }});
    }}
    if (chart.rolling_7d && chart.rolling_7d.length) {{
      datasets.push({{
        label: '7-day average',
        data: chart.rolling_7d,
        borderColor: '#0d9488',
        backgroundColor: 'rgba(13, 148, 136, 0.14)',
        borderWidth: 2.6,
        pointRadius: 0,
        tension: 0.3,
        fill: true,
        order: 1,
      }});
    }}

    new Chart(chartEl, {{
      type: 'line',
      data: {{ labels: chart.labels, datasets }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        spanGaps: true,
        interaction: {{ mode: 'index', intersect: false }},
        plugins: {{
          legend: {{
            display: true,
            position: 'bottom',
            labels: {{
              color: '#6b7280',
              boxWidth: 24,
              padding: 12,
              font: {{ size: 11 }},
            }}
          }},
          tooltip: {{
            callbacks: {{
              label: (ctx) => {{
                if (ctx.parsed.y == null) return null;
                return ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + ' lb';
              }}
            }}
          }}
        }},
        scales: {{
          x: {{ ticks: {{ maxTicksLimit: 6, color: '#6b7280' }}, grid: {{ display: false }} }},
          y: {{ ticks: {{ color: '#6b7280' }}, grid: {{ color: '#eee' }} }}
        }}
      }}
    }});
  }}
}})();
</script>
</body>
</html>
"""


MEAL_ICONS = {"breakfast": "🍳", "lunch": "🥗", "dinner": "🍽", "snack": "🍎"}


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_progress(plan: dict | None, has_weight: bool) -> str:
    if not plan:
        return '<p class="empty">No plan today yet — check back after the next coach run.</p>'
    weight = plan.get("weight")
    if weight and isinstance(weight, dict):
        latest = weight.get("latest_lb")
        avg = weight.get("trailing_7d_avg_lb")
        trend = weight.get("trend_vs_prior_7d_lb")
        latest_html = f"{latest:.1f} lb" if latest is not None else "—"
        avg_html = f"{avg:.1f} lb" if avg is not None else "—"
        trend_class = ""
        trend_html = "—"
        if trend is not None:
            trend_class = "down" if trend < 0 else ("up" if trend > 0 else "")
            sign = "" if trend >= 0 else "−"
            trend_html = f'{sign}{abs(trend):.1f} lb vs prior 7d'
        return f"""
<div class="metric-grid">
  <div class="metric"><div class="label">Latest</div><div class="value">{latest_html}</div><div class="delta">on {weight.get('latest_date', '—')}</div></div>
  <div class="metric"><div class="label">7-day avg</div><div class="value">{avg_html}</div><div class="delta {trend_class}">{trend_html}</div></div>
</div>"""
    if has_weight:
        return ""
    return '<p class="empty">No weight tracking yet — your coach will set this up after intake.</p>'


def render_chart(has_weight: bool) -> str:
    return '<canvas id="weightChart"></canvas>' if has_weight else ""


def render_goals(plan: dict | None) -> str:
    if not plan:
        return ""
    goals = plan.get("goals") or []
    if not goals:
        return '<p class="empty">No goals set yet.</p>'
    out = []
    for g in goals:
        if not isinstance(g, dict):
            continue
        status = (g.get("status") or "tbd").lower()
        title = html_escape(g.get("title") or "")
        note = html_escape(g.get("note") or "")
        out.append(
            f'<div class="goal"><span class="goal-title">{title}</span>'
            f'<span class="goal-status {status}">{status}</span>'
            + (f'<div style="font-size:13px;color:var(--muted);">{note}</div>' if note else "")
            + "</div>"
        )
    return "\n".join(out)


def render_plan(plan: dict | None) -> str:
    if not plan:
        return '<p class="empty">No plan generated yet today.</p>'
    rows: list[str] = []
    workout = plan.get("workout")
    if workout and isinstance(workout, dict):
        title = html_escape(workout.get("title") or "Workout")
        desc = html_escape(workout.get("description") or "")
        details_path = workout.get("details_path")
        embed = (
            f'<details class="embed"><summary>Details</summary>'
            f'<div class="md" data-embed="{html_escape(details_path)}"></div></details>'
            if details_path
            else ""
        )
        rows.append(
            f'<div class="plan-row"><div class="icon">🏋️</div><div class="body">'
            f'<div class="label">Workout</div>'
            f'<div class="text"><strong>{title}</strong> — {desc}</div>{embed}'
            f"</div></div>"
        )
    else:
        rows.append(
            '<div class="plan-row"><div class="icon">🛌</div><div class="body">'
            '<div class="label">Workout</div><div class="text empty">Rest day</div>'
            "</div></div>"
        )
    for meal in plan.get("meals") or []:
        if not isinstance(meal, dict):
            continue
        kind = (meal.get("meal") or "").lower()
        icon = MEAL_ICONS.get(kind, "🍽")
        desc = html_escape(meal.get("description") or "")
        recipe = meal.get("recipe_path")
        embed = (
            f'<details class="embed"><summary>Recipe</summary>'
            f'<div class="md" data-embed="{html_escape(recipe)}"></div></details>'
            if recipe
            else ""
        )
        rows.append(
            f'<div class="plan-row"><div class="icon">{icon}</div><div class="body">'
            f'<div class="label">{kind.capitalize() or "Meal"}</div>'
            f'<div class="text">{desc}</div>{embed}'
            "</div></div>"
        )
    tasks = plan.get("tasks") or []
    if tasks:
        items = "\n".join(f"<li>{html_escape(t)}</li>" for t in tasks if isinstance(t, str))
        rows.append(
            '<div class="plan-row"><div class="icon">✅</div><div class="body">'
            '<div class="label">Tasks</div>'
            f'<ul class="tasks">{items}</ul>'
            "</div></div>"
        )
    return "\n".join(rows)


def render_coach_note(body: str) -> str:
    if not body.strip():
        return ""
    return f'<div class="coach-note md" data-md="coach_note"></div>'


def pretty_date(d: dt.date) -> str:
    return d.strftime("%A, %B ") + str(d.day) + d.strftime(", %Y")


def build_chart(weight_history: list[dict], plan_fm: dict | None) -> dict:
    """Compute the chart datasets: daily, 7-day rolling average, trend line, start, goal."""
    daily = aggregate_daily(weight_history)
    if not daily:
        return {}
    labels = [d["date"] for d in daily]
    rolling = rolling_average(daily, window=7)
    trend = linear_trend(daily)
    start_lb, goal_lb = parse_goal_endpoints(plan_fm)
    n = len(labels)
    return {
        "labels": labels,
        "daily": [d["weight_lb"] for d in daily],
        "rolling_7d": rolling,
        "trend": trend or [],
        "start_lb": start_lb,
        "goal_lb": goal_lb,
        "start_line": [start_lb] * n if start_lb is not None else [],
        "goal_line": [goal_lb] * n if goal_lb is not None else [],
    }


def render_principal(p: dict) -> str:
    plan_fm, plan_body = load_today_plan(p["dir"])
    measurements_csv = p["dir"] / "measurements.csv"
    weight_history = load_weight_history(measurements_csv) if p["key"] == "justin" else []
    chart = build_chart(weight_history, plan_fm)
    has_weight = bool(weight_history) or bool(
        plan_fm and isinstance(plan_fm.get("weight"), dict)
    )

    motd = (plan_fm or {}).get("motd") or "Today is a good day to be steady."
    embeds = collect_inline_files(p["dir"], plan_fm or {})

    payload = {
        "chart": chart,
        "meal_plan": read_or_empty(HOUSEHOLD_DIR / "meal-plan-current.md"),
        "reading_list": read_or_empty(HOUSEHOLD_DIR / "references" / "reading-list.md"),
        "coach_note": plan_body,
        "embeds": embeds,
    }

    today = dt.date.today()
    return HTML_TEMPLATE.format(
        name=p["name"],
        date_pretty=pretty_date(today),
        motd_html=html_escape(motd),
        progress_html=render_progress(plan_fm, has_weight),
        chart_html=render_chart(bool(weight_history)),
        goals_html=render_goals(plan_fm),
        plan_html=render_plan(plan_fm),
        coach_note_html=render_coach_note(plan_body),
        payload_json=json.dumps(payload, ensure_ascii=False),
        generated_at=dt.datetime.now().strftime("%Y-%m-%d %H:%M %Z").strip(),
        principal_key=p["key"],
    )


def main(argv: list[str]) -> int:
    DASHBOARD_DIR.mkdir(exist_ok=True)
    written: list[str] = []
    for p in PRINCIPALS:
        html = render_principal(p)
        out = DASHBOARD_DIR / f"{p['key']}.html"
        out.write_text(html)
        written.append(str(out.relative_to(ROOT)))
    print(f"wrote: {', '.join(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
