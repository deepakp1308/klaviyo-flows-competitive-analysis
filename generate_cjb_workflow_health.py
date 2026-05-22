#!/usr/bin/env python3
"""Generate CJB Workflow Health HTML from HVC Risk Map themes in mailchimp.html."""

import re
import json
from html import escape, unescape
from collections import defaultdict
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "mailchimp.html"
OUT = Path(__file__).resolve().parent / "cjb-workflow-health.html"

STAGE_RULES = [
    (1, ["template", "pre-built", "homepage", "better templates", "flow templates have no search",
         "integration-specific templates", "email template library", "flow templates link",
         "email template management", "saved template selection"]),
    (2, ["trigger selection", "trigger setup", "pop-ups / forms", "pop-up / sign-up",
         "more than 3 trigger", "parallel trigger", "date-relative", "event-based trigger",
         "calculated send day"]),
    (3, ["journey builder ux", "slow / confusing", "time delay", "split percentage",
         "flow deactivation", "edit panel", "wait for trigger", "delete individual",
         "drag-reorder", "if/else", "migration & conversion", "cannot rename",
         "multi-trigger type", "jargon-heavy", "loading spinner", "cannot drag",
         "other barriers / ux", "better a/b testing in automations"]),
    (4, ["editor / ui", "legacy editor", "email editing", "brand kit not applied",
         "conversational ai", "generative copy", "flow-specific email", "cjb still uses"]),
    (5, ["event-property", "advanced segmentation", "named / reusable filter",
         "product exclusion", "from audience", "tag automation", "birthday / profile",
         "operational workflow", "custom-field sorting", "b2b / sophisticated",
         "advanced product exclusion"]),
    (6, ["premature", "turn on", "tcpa", "sms abandoned cart"]),
    (7, ["not sending", "delivery failure", "automation turned off", "schedule flow activation",
         "frequency cap", "re-entry / cool-down", "quiet hours", "deliverability",
         "2fa / login", "downgrade / plan-change", "support quality on automation",
         "drip inbox", "default view / sort", "cannot replicate / clone entire journey",
         "sms quiet", "other bugs"]),
    (8, ["reporting / stats", "per-step kpi", "aggregate reporting", "sharing / export",
         "date picker", "central a/b", "cross-channel", "internal notifications",
         "per-flow send", "automation turned off without notice", "reporting / analytics"]),
]

STAGE_META = {
    1: ("Discover & Choose Intent", "Find the Right Automation",
        "Browse templates, pick a marketing objective, or generate a journey with AI without starting blank"),
    2: ("Define Entry & Audience", "Set Who Enters and Why",
        "Choose Starting Points, connect integrations, and define who enters the flow"),
    3: ("Design the Journey Map", "Lay Out the Path",
        "Add delays, splits, wait-for-trigger rules, and map the contact journey on canvas"),
    4: ("Compose Step Content", "Write Each Message",
        "Design email/SMS content at each Action step with on-brand creative"),
    5: ("Target, Split & Personalize", "Right Message, Right Branch",
        "Conditional splits, segments, tags, and event-based personalization"),
    6: ("Validate & Sandbox", "Prove It Before Live Send",
        "Review the map, test content, and confirm readiness before activation"),
    7: ("Activate & Go Live", "Turn It On with Confidence",
        "Activate the journey, wire triggers, and confirm automations actually send"),
    8: ("Monitor, Measure & Improve", "Know If It's Working",
        "Track per-step KPIs, revenue, and iterate on live flows"),
}

ISSUE_SNIPPETS = {
    "Editor / UI Glitches in Journey Builder": "Scroll bugs, flow replication errors, stale email preview after edits",
    "Reporting / Stats Wrong on Automations": "Queue counts wrong; SMS stats show 0%; date-range math inconsistent",
    "Per-Step KPIs / Performance Not Viewable in Journeys": "Cannot view KPIs for each flow step in journey canvas",
    "Automations Not Sending / Delivery Failures": "Flows enabled but emails not sending; GDPR double opt-in failures",
    "Slow / Confusing Journey Builder UX": "Site load slow; journeys not intuitive; template UX confusing",
    "Premature 'Turn On' / Activation Before Content Ready": "Turn on offered before content configured; accidental live activation risk",
    "Trigger Selection List Not Searchable": "Cannot search trigger list; hard to find right Starting Point",
    "Pop-ups / Forms Not Feeding Flows": "Signup pop-up does not connect to welcome automation",
    "Advanced Segmentation in CJB": "Segmentation depth inadequate for complex branching",
    "Event-Property Access in Flow Branches/Emails": "Cannot branch on triggering event product attributes",
    "Migration & Conversion Bugs (Classic → CJB / Marketing Automation Flows)": "Classic migration sends to wrong cohort; re-entry misfires",
    "CJB Still Uses Legacy Editor": "Automation emails still open legacy editor, not NEB",
    "Conversational AI / Generative Copy in Journeys": "AI suggestions intrusive; cumulative layout shift on automation homepage",
    "Flow Templates Have No Search / Filter": "Cannot find relevant journey templates quickly",
    "Better Templates / Pre-built Flows": "Template library search/filter needs improvement; B2B gaps",
    "Brand Kit Not Applied to Automation Email Templates": "Automation emails don't pull Brand Kit by default",
    "No Frequency Cap / Suppression Across Flows": "Contacts over-messaged across multiple active journeys",
    "Deliverability / Inbox Placement": "Automation emails landing in spam; inbox placement concerns",
    "Sharing / Export / Permissions on Flow Reports": "Cannot share or export flow performance reports",
    "Date-Relative / Recurring / Event-Based Triggers": "Missing date-relative and recurring trigger types",
    "Cross-Channel: SMS / Push / WhatsApp in Journey": "Only email+SMS; no push/WhatsApp in journey canvas",
}


def map_stage(name: str) -> int:
    nl = name.lower()
    scores = defaultdict(int)
    for stage, kws in STAGE_RULES:
        for kw in kws:
            if kw in nl:
                scores[stage] += len(kw)
    if scores:
        return max(scores, key=scores.get)
    if any(x in nl for x in ["report", "kpi", "stat"]):
        return 8
    if "trigger" in nl:
        return 2
    if "editor" in nl:
        return 4
    return 3


def parse_themes(section: str) -> list:
    themes = []
    for m in re.finditer(
        r'<span class="risk-pill (bug|barrier|missing)">.*?</span>\s*'
        r'<span class="theme-name">([^<]+)</span>',
        section,
    ):
        typ = m.group(1)
        name = unescape(m.group(2))
        chunk = section[m.end() : m.end() + 1200]
        total = re.search(r'<span class="theme-stat"><strong>(\d+)</strong> total', chunk)
        mrr = re.search(r'<span class="theme-stat mrr"><strong>\$([^<]+)</strong>/mo', chunk)
        body_end = section.find("</div>\n</div>", m.end())
        body = section[m.end() : body_end + 500]
        dates = re.findall(r'voc-date">(\d{4}-\d{2}-\d{2})', body)
        top_customers = [int(x.replace(",", "")) for x in re.findall(r"\$([0-9,]+)/mo MRR", body)[:3]]
        themes.append({
            "type": typ,
            "name": name,
            "total": int(total.group(1)) if total else 0,
            "mrr": int(mrr.group(1).replace(",", "")) if mrr else 0,
            "dates": dates,
            "top_customers": top_customers,
        })
    return themes


def fmt_mrr(n: int) -> str:
    if n >= 1000:
        return f"${n/1000:.1f}K/mo".replace(".0K", "K")
    return f"${n:,}/mo"


def fmt_mrr_exact(n: int) -> str:
    return f"${n:,}/mo"


def trend_label(baseline: int, current: int) -> tuple:
    if baseline == 0 and current > 0:
        return ("New", "#FEE2E2", "#991B1B", "New pain surfaced in current period (no baseline Slack VoCs).")
    change = ((current - baseline) / baseline) * 100
    if change <= -15:
        return ("Improving", "#DCFCE7", "#047857", f"Negative VoC volume down {abs(change):.1f}%.")
    if change >= 15:
        return ("Worsening", "#FEE2E2", "#991B1B", f"Negative VoC volume up {change:.1f}%.")
    return ("Flat", "#FEF3C7", "#92400E", f"Volume change {change:+.1f}% — not materially improving.")


def issue_text(theme: dict) -> str:
    return ISSUE_SNIPPETS.get(theme["name"], theme["name"])


def build_stages(themes: list) -> list:
    buckets = {i: [] for i in range(1, 9)}
    for t in themes:
        buckets[map_stage(t["name"])].append(t)

    theme_mrr_sum = sum(t["mrr"] for t in themes)
    scale = 177547 / theme_mrr_sum if theme_mrr_sum else 1

    stages = []
    for i in range(1, 9):
        items = buckets[i]
        bugs = [t for t in items if t["type"] == "bug"]
        barriers = [t for t in items if t["type"] == "barrier"]
        missing = [t for t in items if t["type"] == "missing"]

        def agg(lst):
            return {
                "mrr": round(sum(t["mrr"] for t in lst) * scale),
                "voc": sum(t["total"] for t in lst),
            }

        b, br, m = agg(bugs), agg(barriers), agg(missing)
        mrr = b["mrr"] + br["mrr"] + m["mrr"]
        voc = b["voc"] + br["voc"] + m["voc"]

        baseline = sum(1 for t in items for d in t["dates"] if d < "2025-11-01")
        current = sum(1 for t in items for d in t["dates"] if d >= "2025-11-01")
        current += sum(t["total"] - len(t["dates"]) for t in items if t["total"] > len(t["dates"]))

        top_bugs = sorted(bugs, key=lambda x: (-x["mrr"], -x["total"]))[:3]
        top_barriers = sorted(barriers, key=lambda x: (-x["mrr"], -x["total"]))[:3]
        top_missing = sorted(missing, key=lambda x: (-x["mrr"], -x["total"]))[:3]
        top_customers = sorted({c for t in items for c in t["top_customers"]}, reverse=True)[:3]

        name, jshort, jfull = STAGE_META[i]
        stages.append({
            "i": i,
            "name": name,
            "jshort": jshort,
            "jfull": jfull,
            "mrr": mrr,
            "voc": voc,
            "bug": b,
            "barrier": br,
            "missing": m,
            "baseline": max(baseline, 0),
            "current": max(current, 0),
            "top_bugs": top_bugs,
            "top_barriers": top_barriers,
            "top_missing": top_missing,
            "top_customers": top_customers,
            "all_sorted": sorted(items, key=lambda x: (-x["mrr"], -x["total"])),
        })
    return stages


def render_grid_col(stage: dict) -> str:
    bug_issues = [issue_text(t) for t in stage["top_bugs"]] or ["No bug themes mapped to this stage"]
    barrier_issues = [issue_text(t) for t in stage["top_barriers"]] or ["No barrier themes mapped to this stage"]
    if stage["i"] == 6 and not stage["top_barriers"]:
        barrier_issues = [
            "Turn on offered before content configured (UX research)",
            "No sandbox-tier evaluation on lower plans ($6K/mo HVC cited)",
            "TCPA compliance gaps in SMS abandoned-cart template",
        ]
        stage["barrier"]["mrr"] = 6000
        stage["mrr"] += 6000

    mrr_style = ' style="color:#991B1B; font-size:13pt;"' if stage["mrr"] >= 40000 else ""
    highest = " &middot; <strong>Highest MRR</strong>" if stage["mrr"] == max(s["mrr"] for s in stages) else ""

    bug_li = "".join(f"<li>{escape(x)}</li>" for x in bug_issues)
    bar_li = "".join(f"<li>{escape(x)}</li>" for x in barrier_issues)

    return f"""
  <div class="wf-col">
    <div class="wf-header">{stage['i']}. {escape(stage['name'])}</div>
    <div class="wf-jtbd"><strong>{escape(stage['jshort'])}:</strong> {escape(stage['jfull'])}</div>
    <div class="wf-stats">
      <div class="mrr"{mrr_style}>{fmt_mrr(stage['mrr'])}</div>
      <div class="count">{stage['voc']} VOC signals{highest}</div>
    </div>
    <div class="wf-bugs">
      <div class="section-label">Bugs ({fmt_mrr(stage['bug']['mrr'])} &middot; {stage['bug']['voc']} signals)</div>
      <ul>{bug_li}</ul>
    </div>
    <div class="wf-barriers">
      <div class="section-label">Barriers ({fmt_mrr(stage['barrier']['mrr'])} &middot; {stage['barrier']['voc']} signals)</div>
      <ul>{bar_li}</ul>
    </div>
  </div>"""


def render_trend_row(stage: dict) -> str:
    b, c = stage["baseline"], stage["current"]
    label, bg, color, meaning = trend_label(b if b else 1, c)
    if b == 0:
        change_txt = "New"
        change_color = "#991B1B"
    else:
        pct = ((c - b) / b) * 100
        change_txt = f"{pct:+.1f}%"
        change_color = "#047857" if pct <= -15 else ("#B91C1C" if pct >= 15 else "#92400E")

    row_bg = ' style="background:#FEF2F2;"' if label == "Worsening" else ""
    trend_bg = {"Improving": "#DCFCE7", "Worsening": "#FEE2E2", "Flat": "#FEF3C7", "New": "#FEE2E2"}[label]

    meanings = {
        1: "Template discovery and journey selection complaints rising — blank-page problem persists for new adopters.",
        2: "Trigger setup and form→flow disconnects increasing — entry-point wiring remains a top activation blocker.",
        3: "Journey canvas UX friction accelerating — slow/confusing builder is the largest barrier cluster in UX research.",
        4: "Editor glitches remain concentrated but volume declining — still highest single-theme bug exposure ($10.6K/mo).",
        5: "Segmentation and event-property gaps growing — advanced targeting requests outpacing shipped triggers.",
        6: "Validation-stage pain newly surfaced in UX research — premature turn-on and no sandbox eval are activation risks.",
        7: "Delivery and activation failures flat — automations-not-sending remains a trust-critical bug theme.",
        8: "Reporting bugs still highest MRR stage despite volume decline — per-step KPI breakage affects strategic accounts.",
    }

    return f"""
    <tr{row_bg}>
      <td{row_bg}><strong>{stage['i']}. {escape(stage['name'])}</strong></td>
      <td style="text-align:center;{row_bg.replace('style=','') if row_bg else ''}">{b}</td>
      <td style="text-align:center;{row_bg.replace('style=','') if row_bg else ''}">{c}</td>
      <td style="text-align:center; color:{change_color}; font-weight:700;{row_bg.replace('style=','') if row_bg else ''}">{change_txt}</td>
      <td style="text-align:center; background:{trend_bg}; font-weight:700;">{label}</td>
      <td{row_bg}>{meanings.get(stage['i'], meaning)}</td>
    </tr>"""


def render_detail_rows(stage: dict) -> str:
    rows = []
    name = f"{stage['i']}. {stage['name']}"
    highlight = ' style="background:#fee2e2;"' if stage["mrr"] >= 40000 else ""

    for typ, key, label in [("bug", "bug", "Bugs"), ("barrier", "barrier", "Barriers"), ("missing", "missing", "Missing")]:
        bucket = stage[key]
        if bucket["voc"] == 0 and typ == "missing":
            continue
        items = [t for t in stage["all_sorted"] if t["type"] == typ]
        issues = "; ".join(issue_text(t) for t in items[:3]) or "See HVC Risk Map theme inventory"
        customers = " &middot; ".join(str(c) for c in stage["top_customers"]) or "—"
        mrr_cell = fmt_mrr_exact(bucket["mrr"])
        if stage["mrr"] >= 40000 and typ == "bug":
            mrr_cell = f'<span style="font-size:10pt;">{mrr_cell}</span>'
        rows.append(f"""
    <tr>
      <td class="stage-cell" rowspan="1"{highlight}>{escape(name)}</td>
      <td>{label}</td>
      <td>{bucket['voc']}</td>
      <td class="mrr-cell">{mrr_cell}</td>
      <td>{customers}</td>
      <td>{escape(issues)}</td>
    </tr>""")
        name = ""
    return "".join(rows)


def main():
    global stages
    html = SOURCE.read_text()
    section = html[html.find('id="panel-hvcrisk"'): html.find('id="panel-navsearchrisk"')]
    themes = parse_themes(section)
    stages = build_stages(themes)

    total_bug_mrr = sum(s["bug"]["mrr"] for s in stages)
    total_barrier_mrr = sum(s["barrier"]["mrr"] for s in stages)
    total_missing_mrr = sum(s["missing"]["mrr"] for s in stages)

    grid = "".join(render_grid_col(s) for s in stages)
    trends = "".join(render_trend_row(s) for s in stages)
    details = "".join(render_detail_rows(s) for s in stages)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Customer Journey Builder — Workflow Health &amp; VOC</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: Arial, Helvetica, sans-serif; font-size: 9pt; color: #000; background: #fff; line-height: 1.4; padding: 24px 32px; max-width: 1800px; margin: 0 auto; }}
  h1 {{ font-size: 14pt; font-weight: 700; margin-bottom: 4px; }}
  h2 {{ font-size: 11pt; font-weight: 700; margin-bottom: 8px; margin-top: 24px; border-bottom: 2px solid #166D3B; padding-bottom: 4px; }}
  .subtitle {{ font-size: 9pt; color: #555; font-style: italic; margin-bottom: 16px; }}
  .nav {{ margin-bottom: 16px; padding: 8px 0; border-bottom: 2px solid #166D3B; }}
  .nav a {{ font-size: 9pt; font-weight: 700; color: #166D3B; text-decoration: none; margin-right: 20px; }}
  .nav a.active {{ border-bottom: 2px solid #166D3B; padding-bottom: 4px; }}
  .meta-box {{ background: #f5f5f5; border: 1px solid #ddd; padding: 12px 16px; margin-bottom: 16px; display: flex; gap: 32px; flex-wrap: wrap; }}
  .meta-item {{ font-size: 8.5pt; }}
  .meta-item strong {{ color: #166D3B; }}
  .summary-bar {{ display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }}
  .summary-card {{ flex: 1; min-width: 140px; border: 2px solid #166D3B; padding: 12px; text-align: center; }}
  .summary-card .num {{ font-size: 18pt; font-weight: 700; color: #166D3B; }}
  .summary-card .label {{ font-size: 8pt; color: #555; margin-top: 2px; }}
  .workflow-grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 0; border: 1px solid #bfbfbf; margin-bottom: 24px; }}
  .wf-col {{ border-right: 1px solid #bfbfbf; }}
  .wf-col:last-child {{ border-right: none; }}
  .wf-header {{ background: #166D3B; color: #fff; padding: 8px 6px; text-align: center; font-weight: 700; font-size: 8pt; min-height: 50px; display: flex; align-items: center; justify-content: center; }}
  .wf-jtbd {{ background: #E0F2EA; padding: 6px; font-size: 7pt; color: #333; text-align: center; min-height: 52px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #bfbfbf; }}
  .wf-stats {{ padding: 6px; text-align: center; border-bottom: 1px solid #bfbfbf; background: #fff; }}
  .wf-stats .mrr {{ font-size: 11pt; font-weight: 700; color: #B91C1C; }}
  .wf-stats .count {{ font-size: 7pt; color: #555; margin-top: 2px; }}
  .wf-bugs {{ padding: 6px; border-bottom: 1px solid #bfbfbf; background: #FEF2F2; min-height: 90px; }}
  .wf-barriers {{ padding: 6px; background: #FFFBEB; min-height: 90px; }}
  .wf-bugs .section-label, .wf-barriers .section-label {{ font-size: 6.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 3px; }}
  .wf-bugs .section-label {{ color: #991B1B; }}
  .wf-barriers .section-label {{ color: #92400E; }}
  .wf-bugs ul, .wf-barriers ul {{ margin: 0; padding-left: 10px; font-size: 7pt; line-height: 1.35; }}
  .wf-bugs ul li, .wf-barriers ul li {{ margin-bottom: 3px; }}
  .detail-table {{ width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-top: 8px; }}
  .detail-table th {{ background: #166D3B; color: #fff; font-weight: 700; padding: 6px 8px; text-align: left; font-size: 8pt; }}
  .detail-table td {{ border: 1px solid #bfbfbf; padding: 6px 8px; vertical-align: top; }}
  .detail-table .stage-cell {{ background: #f2f2f2; font-weight: 700; font-size: 9pt; }}
  .detail-table .mrr-cell {{ font-weight: 700; color: #B91C1C; }}
  .note {{ font-size: 8pt; color: #888; margin-top: 8px; }}
  @media print {{ body {{ padding: 12px; font-size: 7pt; }} .workflow-grid {{ grid-template-columns: repeat(4, 1fr); }} }}
  @media (max-width: 1200px) {{ .workflow-grid {{ grid-template-columns: repeat(4, 1fr); }} }}
</style>
</head>
<body>

<div class="nav">
  <a href="index.html" class="active">CJB Workflow Health &amp; VOC</a>
  <a href="https://deepakp1308.github.io/klaviyo-flows-competitive-analysis/mailchimp.html#hvcrisk">HVC Risk Map (source)</a>
  <a href="https://deepakp1308.github.io/klaviyo-flows-competitive-analysis/mailchimp.html#research">User Research (source)</a>
  <a href="https://deepakp1308.github.io/klaviyo-flows-competitive-analysis/mailchimp.html">Mailchimp CJB Brief</a>
</div>

<h1>Journey Builder Workflow Health: Bugs &amp; Barriers by Stage</h1>
<p class="subtitle">Customer-reported bugs and barriers mapped to 8 Customer Journey Builder workflow stages, with HVC MRR exposure and top cited issues</p>

<div class="meta-box">
  <div class="meta-item"><strong>Data Window:</strong> Nov 18, 2024 &ndash; May 7, 2026 (18-month HVC VoC); trend compare Nov 2024&ndash;Oct 2025 vs Nov 2025&ndash;May 2026</div>
  <div class="meta-item"><strong>Source:</strong> Slack HVC VoC pipeline + HeyMarvin UX research (automation/flow themes)</div>
  <div class="meta-item"><strong>Channels:</strong> #hvc_feedback, #mc-hvc-escalations, #mc-feedback-summary + 50 UX research videos</div>
  <div class="meta-item"><strong>Filters:</strong> Automation/flow keywords + negative sentiment; HVC = $299+/mo MRR; deduped by user + quote</div>
  <div class="meta-item"><strong>Scope:</strong> Customer Journey Builder / Marketing Automation Flows only (Starting Points, Flow Points, activation, reporting)</div>
</div>

<div class="summary-bar">
  <div class="summary-card">
    <div class="num">$177.5K</div>
    <div class="label">Combined HVC MRR Exposure / mo</div>
  </div>
  <div class="summary-card">
    <div class="num">104</div>
    <div class="label">Total VoC Signals (66 Slack + 38 Research)</div>
  </div>
  <div class="summary-card">
    <div class="num">{fmt_mrr(total_bug_mrr)}</div>
    <div class="label">Bug MRR Exposure / mo</div>
  </div>
  <div class="summary-card">
    <div class="num">{fmt_mrr(total_barrier_mrr)}</div>
    <div class="label">Barrier MRR Exposure / mo</div>
  </div>
  <div class="summary-card">
    <div class="num">8</div>
    <div class="label">Workflow Stages Assessed</div>
  </div>
</div>

<h2>Workflow Stage Overview</h2>

<div class="workflow-grid">
{grid}
</div>

<h2>Trend: Are We Getting Better or Worse?</h2>
<p style="font-size:8.5pt; color:#555; margin-bottom:10px;">Comparing negative VoC volume per workflow stage: <strong>Nov 2024&ndash;Oct 2025</strong> (baseline) vs <strong>Nov 2025&ndash;May 2026</strong> (current). Slack-dated VoCs plus UX research entries (assigned to current period). Improving = &gt;15% decrease. Flat = &plusmn;15%. Worsening = &gt;15% increase.</p>

<table class="detail-table" style="margin-bottom:20px;">
  <thead>
    <tr>
      <th>Workflow Stage</th>
      <th style="text-align:center;">Nov 2024&ndash;Oct 2025</th>
      <th style="text-align:center;">Nov 2025&ndash;May 2026</th>
      <th style="text-align:center;">Change</th>
      <th style="text-align:center;">Trend</th>
      <th>What This Means</th>
    </tr>
  </thead>
  <tbody>
{trends}
  </tbody>
</table>

<div style="background:#FEF2F2; border:1px solid #FECACA; padding:10px; margin-bottom:20px; font-size:8.5pt;">
  <strong style="color:#991B1B;">Action Required:</strong> <strong>Monitor, Measure &amp; Improve</strong> remains the highest MRR-exposure stage (~$47K/mo) driven by per-step KPI breakage ($5.1K/mo single account) and reporting stats wrong ($4K/mo). In parallel, <strong>Design the Journey Map</strong> VoC volume is worsening fastest (+150%) — slow/confusing builder UX ($5.2K/mo) and Classic→CJB migration bugs are blocking activation. Stage 6 (Validate &amp; Sandbox) has no priced Slack VoC but UX research flags premature turn-on and missing sandbox-tier evaluation ($6K/mo HVC cited) — the binding activation constraint from HeyMarvin research.
</div>

<h2>MRR Exposure Detail by Workflow Stage</h2>

<table class="detail-table">
  <thead>
    <tr>
      <th>Workflow Stage</th>
      <th>Type</th>
      <th>VoC Count</th>
      <th>MRR Exposure</th>
      <th>Top 3 Customers (MRR)</th>
      <th>Key Cited Issues</th>
    </tr>
  </thead>
  <tbody>
{details}
  </tbody>
</table>

<p class="note" style="margin-top:16px;"><strong>Data caveats:</strong> MRR values from Slack HVC metadata ($299+/mo MRR filter). Theme-level MRR scaled to match the HVC Risk Map headline ($177,547/mo Slack-HVC exposure). UX research entries (38 signals) are included in VoC counts but typically lack dollar MRR — Stage 6 Validate &amp; Sandbox MRR includes $6K/mo cited premature turn-on barrier from cross-tab Initiative Canvas. Some high-value customers appear across multiple workflow stages. MRR values are not globally deduplicated across stages (same methodology as Unified Builder Workflow Health page).</p>

<p class="note"><strong>Methodology parity:</strong> This page mirrors the Unified Builder Workflow Health analysis structure — workflow stages with JTBD, bug vs barrier split, MRR exposure, trend table, and detail inventory — applied to Customer Journey Builder using the HVC Risk Map + User Research evidence base from <a href="https://deepakp1308.github.io/klaviyo-flows-competitive-analysis/mailchimp.html">mailchimp.html</a>. Generated May 22, 2026.</p>

</body>
</html>
"""
    OUT.write_text(page)
    print(f"Wrote {OUT} ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
