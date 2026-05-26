#!/usr/bin/env python3
"""Build cjb-scrawler-report.html from JSONL findings in cjb-scrawler/findings/."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINDINGS_DIR = ROOT / "cjb-scrawler" / "findings"
OUT_HTML = ROOT / "cjb-scrawler-report.html"
FIX_BACKLOG = ROOT / "cjb-scrawler" / "fix-backlog.md"

STAGE_META = {
    1: ("Discover & Choose Intent", "Templates, objectives, AI journey start"),
    2: ("Define Entry & Audience", "Starting points, triggers, audience"),
    3: ("Design the Journey Map", "Delays, splits, canvas layout"),
    4: ("Compose Step Content", "Email/SMS content per step"),
    5: ("Target, Split & Personalize", "Branches, segments, tags"),
    6: ("Validate & Sandbox", "Review before activation"),
    7: ("Activate & Go Live", "Turn on, triggers wired"),
    8: ("Monitor, Measure & Improve", "Reporting, KPIs"),
}

KNOWN_THEME_MAP = {
    "trigger": "Trigger Selection List Not Searchable",
    "search": "Trigger Selection List Not Searchable",
    "turn on": "Premature 'Turn On' / Activation Before Content Ready",
    "template": "Better Templates / Pre-built Flows",
    "e-commerce": "Better Templates / Pre-built Flows",
    "ecommerce": "Better Templates / Pre-built Flows",
    "scroll": "Editor / UI Glitches in Journey Builder",
    "legacy editor": "CJB Still Uses Legacy Editor",
    "neb": "CJB Still Uses Legacy Editor",
    "brand kit": "Brand Kit Not Applied to Automation Email Templates",
    "frequency": "No Frequency Cap / Suppression Across Flows",
    "report": "Reporting / Stats Wrong on Automations",
    "delay": "Slow / Confusing Journey Builder UX",
    "hour": "Slow / Confusing Journey Builder UX",
    "segment": "Advanced Segmentation in CJB",
    "pop-up": "Pop-ups / Forms Not Feeding Flows",
    "popup": "Pop-ups / Forms Not Feeding Flows",
}


def symptom_hash(title: str, stage: int) -> str:
    norm = re.sub(r"\s+", " ", title.lower().strip())
    return hashlib.sha256(f"{stage}:{norm}".encode()).hexdigest()[:12]


def infer_known_theme(title: str, observed: str) -> str | None:
    blob = f"{title} {observed}".lower()
    for key, theme in KNOWN_THEME_MAP.items():
        if key in blob:
            return theme
    return None


def load_findings() -> list[dict]:
    rows: list[dict] = []
    if not FINDINGS_DIR.is_dir():
        return rows
    for path in sorted(FINDINGS_DIR.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def dedupe_issues(rows: list[dict]) -> list[dict]:
    """Keep worst severity per symptom_hash for fail/blocked only."""
    by_hash: dict[str, dict] = {}
    sev_rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "—": 9}
    for r in rows:
        if r.get("status") == "pass":
            continue
        h = r.get("symptom_hash") or symptom_hash(r.get("title", ""), r.get("stage", 0))
        r["symptom_hash"] = h
        prev = by_hash.get(h)
        if not prev or sev_rank.get(r.get("severity", "P3"), 9) < sev_rank.get(
            prev.get("severity", "P3"), 9
        ):
            by_hash[h] = r
    return sorted(
        by_hash.values(),
        key=lambda x: (sev_rank.get(x.get("severity", "P3"), 9), x.get("stage", 0)),
    )


def render_step_rows(rows: list[dict]) -> str:
    parts = []
    for r in rows:
        st = r.get("stage", 0)
        st_name = STAGE_META.get(st, ("", ""))[0]
        sev = r.get("severity", "—")
        status = r.get("status", "")
        cls = "pass" if status == "pass" else "fail" if status == "fail" else "blocked"
        parts.append(
            f"<tr class='{cls}'>"
            f"<td>{escape(str(r.get('persona', '')))}</td>"
            f"<td><code>{escape(str(r.get('step_id', '')))}</code></td>"
            f"<td>{st}</td><td>{escape(st_name)}</td>"
            f"<td>{escape(status)}</td><td><strong>{escape(sev)}</strong></td>"
            f"<td>{escape(r.get('title', ''))}</td>"
            f"<td>{escape(r.get('observed', '')[:280])}</td>"
            f"</tr>"
        )
    return "\n".join(parts) if parts else "<tr><td colspan='8'>No findings yet. Run CJB Scrawler.</td></tr>"


def render_issue_cards(issues: list[dict]) -> str:
    if not issues:
        return "<p>No fail/blocked findings recorded.</p>"
    parts = []
    for i, r in enumerate(issues, 1):
        known = r.get("known_theme") or infer_known_theme(
            r.get("title", ""), r.get("observed", "")
        )
        novel = r.get("novel", not known)
        fix = r.get("fix_proposal") or {}
        parts.append(
            f"<div class='issue-card'>"
            f"<h3>{i}. [{escape(r.get('severity', ''))}] {escape(r.get('title', ''))}</h3>"
            f"<p><strong>Persona:</strong> {escape(str(r.get('persona')))} · "
            f"<strong>Stage {r.get('stage')}:</strong> {escape(STAGE_META.get(r.get('stage', 0), ('', ''))[0])}</p>"
            f"<p><strong>Observed:</strong> {escape(r.get('observed', ''))}</p>"
            f"<p><strong>Expected:</strong> {escape(r.get('expected', ''))}</p>"
            f"<p><strong>HVC theme:</strong> {escape(known or '—')} "
            f"({'novel' if novel else 'known'})</p>"
        )
        if fix.get("proposed_fix"):
            lane = r.get("engineering_lane") or fix.get("engineering_lane") or "unknown"
            effort = fix.get("effort", "—")
            parts.append(
                f"<p><strong>Proposed fix:</strong> {escape(fix['proposed_fix'])}</p>"
                f"<p><strong>Lane:</strong> {escape(str(lane))} · "
                f"<strong>Effort:</strong> {escape(str(effort))}</p>"
            )
        if r.get("roadmap_link"):
            parts.append(f"<p><strong>Roadmap:</strong> {escape(r['roadmap_link'])}</p>")
        parts.append("</div>")
    return "\n".join(parts)


def stage_summary(rows: list[dict]) -> str:
    counts: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if r.get("status") == "pass":
            continue
        counts[r.get("stage", 0)][r.get("severity", "P3")] += 1
    lines = ["<table><tr><th>Stage</th><th>Name</th><th>P0</th><th>P1</th><th>P2</th><th>P3</th></tr>"]
    for st in range(1, 9):
        c = counts.get(st, {})
        name = STAGE_META[st][0]
        lines.append(
            f"<tr><td>{st}</td><td>{escape(name)}</td>"
            f"<td class='num'>{c.get('P0', 0)}</td><td class='num'>{c.get('P1', 0)}</td>"
            f"<td class='num'>{c.get('P2', 0)}</td><td class='num'>{c.get('P3', 0)}</td></tr>"
        )
    lines.append("</table>")
    return "\n".join(lines)


def main() -> None:
    rows = load_findings()
    issues = dedupe_issues(rows)
    run_ids = sorted({r.get("run_id", "") for r in rows if r.get("run_id")})
    personas = sorted({r.get("persona", "") for r in rows if r.get("persona")})
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    n_pass = sum(1 for r in rows if r.get("status") == "pass")
    n_fail = sum(1 for r in rows if r.get("status") == "fail")
    n_blocked = sum(1 for r in rows if r.get("status") == "blocked")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CJB Scrawler — Live UX Audit Report</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10pt; color: #000; background: #fff;
    line-height: 1.45; padding: 24px 32px; max-width: 1200px; margin: 0 auto; }}
  h1 {{ font-size: 16pt; margin-bottom: 6px; }}
  h2 {{ font-size: 12pt; margin: 20px 0 8px; border-bottom: 2px solid #000; padding-bottom: 4px; }}
  .subtitle {{ color: #555; font-style: italic; margin-bottom: 16px; font-size: 9pt; }}
  .nav {{ margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #000; }}
  .nav a {{ margin-right: 12px; color: #000; font-weight: 700; font-size: 9pt; }}
  .kpi-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 12px 0; }}
  .kpi {{ border: 1px solid #ccc; padding: 10px 14px; min-width: 120px; }}
  .kpi .v {{ font-size: 18pt; font-weight: 700; }}
  .kpi .l {{ font-size: 8pt; color: #555; text-transform: uppercase; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 9pt; margin-top: 8px; }}
  th, td {{ border: 1px solid #bfbfbf; padding: 6px 8px; vertical-align: top; text-align: left; }}
  th {{ background: #d9d9d9; }}
  tr.fail td {{ background: #fde8e8; }}
  tr.blocked td {{ background: #fef3e0; }}
  tr.pass td {{ background: #f5f5f5; }}
  .num {{ text-align: right; }}
  .issue-card {{ border: 1px solid #ccc; padding: 12px; margin: 10px 0; }}
  .issue-card h3 {{ font-size: 11pt; margin-bottom: 6px; }}
  .method {{ background: #f5f5f5; border-left: 4px solid #000; padding: 10px 14px; margin: 12px 0; font-size: 9pt; }}
</style>
</head>
<body>
<nav class="nav">
  <a href="mailchimp.html">Mailchimp dossier</a>
  <a href="cjb-workflow-health.html">CJB workflow health</a>
  <a href="cjb-repo-analysis.html">CJB repo forensics</a>
</nav>
<h1>CJB Scrawler — Live UX Audit Report</h1>
<p class="subtitle">Generated {escape(generated)} · Qualitative N=1 scripted journeys (not statistical VoC). Draft-only, test audience.</p>
<div class="method">
  <strong>Method:</strong> Browser automation via CJB Scrawler skill against live Mailchimp CJB.
  Personas: e-commerce welcome + first-purchase incentive; ProServ lead nurture + consultation CTA.
  Mapped to 8-stage taxonomy in <code>generate_cjb_workflow_health.py</code>.
</div>
<div class="kpi-row">
  <div class="kpi"><div class="v">{len(rows)}</div><div class="l">Step logs</div></div>
  <div class="kpi"><div class="v">{n_pass}</div><div class="l">Pass</div></div>
  <div class="kpi"><div class="v">{n_fail}</div><div class="l">Fail</div></div>
  <div class="kpi"><div class="v">{n_blocked}</div><div class="l">Blocked</div></div>
  <div class="kpi"><div class="v">{len(issues)}</div><div class="l">Deduped issues</div></div>
</div>
<p><strong>Run IDs:</strong> {escape(", ".join(run_ids) or "—")} · <strong>Personas:</strong> {escape(", ".join(personas) or "—")}</p>

<h2>Issues by workflow stage</h2>
{stage_summary(rows)}

<h2>Deduped issue cards + fix direction</h2>
{render_issue_cards(issues)}

<h2>All step logs</h2>
<table>
<tr><th>Persona</th><th>Step</th><th>#</th><th>Stage name</th><th>Status</th><th>Sev</th><th>Title</th><th>Observed (excerpt)</th></tr>
{render_step_rows(rows)}
</table>
<p class="subtitle" style="margin-top:24px;">Regenerate: <code>python3 scripts/build_cjb_scrawler_report.py</code></p>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(rows)} rows, {len(issues)} deduped issues)")


if __name__ == "__main__":
    main()
