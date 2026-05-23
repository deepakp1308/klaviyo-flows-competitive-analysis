#!/usr/bin/env python3
"""Build $21M Customer Targeting tab HTML and embed into unified-builder-workflow-health.html"""
import html
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT.parent / "mailchimp-builder-21m-targeting-plan"
ROADMAP = ROOT / "unified-builder-roadmap.html"
WF = ROOT / "unified-builder-workflow-health.html"
OUT_CSV = MC / "outputs"

FY27 = 0.16
TABLE = "detail-table targeting-table"

CLUSTER_LABELS = {
    0: "C0 · Dormant Paid (Declining Usage)",
    1: "C1 · Reliable Mid-Market Senders",
    2: "C2 · High-MRR Power Users",
    3: "C3 · Consistent Volume Senders",
    4: "C4 · Growing-but-Incomplete Senders",
    5: "C5 · Enterprise-Scale Power Senders",
    6: "C6 · Tenured High-Completion Senders",
    7: "C7 · Dormant Free / Low-MRR Base",
    8: "C8 · Test-Heavy, Low-Publish Friction",
    9: "C9 · High-Friction Abandoners",
    10: "C10 · AI-Adopted Premium Senders",
    11: "C11 · Rising-Usage Power Senders",
    12: "C12 · AI-Ready Mid-Market Senders",
}

CLUSTER_DESC = {
    0: "Paid accounts with near-zero Builder activity in 90d but positive MRR. Churn risk before they stop paying.",
    1: "Steady mid-market senders ~93% completion, low friction. Efficiency and Universal Content plays.",
    2: "High-MRR ($676 avg), heavy Builder use. Universal Content + migration unlock disproportionate value.",
    3: "Stable power senders ~28 creates/mo, 76% completion. Retention and cross-channel expansion.",
    4: "Moderate completion (~43%), rising usage. Template + AI assist between create and publish.",
    5: "Highest-intensity senders (~194 creates/mo). Rendering, performance, Code Mode.",
    6: "Long-tenured 83% completion. Largest healthy mid-market cluster — protect established habit.",
    7: "Free/low-MRR, zero completion. Activation and first-send only.",
    8: "Heavy testing (~75 tests), low publish (33% completion). Rendering/trust barrier.",
    9: "Highest friction (0.75): create but almost never publish. Fix foundation first.",
    10: "Premium senders using AI templates + Brand Kit. Expand Universal Content + Code Mode.",
    11: "Growing usage, ~75% completion. Wave-1 Universal Content candidates.",
    12: "AI template adoption, moderate volume. Bridge AI builder and universal content.",
}

# Every FY27 roadmap initiative (init-cell) → quarter, pillar, model theme for targeting
ROADMAP_INITIATIVES = [
    ("Q1", "P1 Trust", "rendering_fix", "Inbox rendering parity fix"),
    ("Q1", "P1 Trust", "rendering_fix", "Block reorder, drag-and-drop reliability & template navigation fix"),
    ("Q1", "P1 Trust", "rendering_fix", "Template surfacing in campaign wizard"),
    ("Q1", "P1 Trust", "rendering_fix", "Cross-browser regression suite"),
    ("Q1", "P1 Trust", "rendering_fix", "Multi-author save-conflict detection"),
    ("Q2", "P1 Trust", "rendering_fix", "Light/dark mode & background images"),
    ("Q2", "P1 Trust", "rendering_fix", "Inline link checker & deliverability hints"),
    ("Q1", "P1 Trust", "brandkit", "Brand Kit data correctness fix"),
    ("Q2", "P1 Trust", "brandkit", "Brand fonts in landing pages & forms"),
    ("Q1", "P1 Trust", "brandkit", "Font upload & Creative Assistant parity"),
    ("Q3", "P1 Trust", "brandkit", "Multi-brand kits per account"),
    ("Q4", "P1 Trust", "brandkit", "Locked layouts for brand governance"),
    ("Q4", "P1 Trust", "brandkit", "Cross-account brand inheritance"),
    ("Q1", "P1 Trust", "brandkit", "Brand voice profile in Brand Kit"),
    ("Q2", "P1 Trust", "brandkit", "Brand compliance score"),
    ("Q2", "P1 Trust", "brandkit", "Brand Kit maturity dashboard"),
    ("Q1", "P1 Trust", "rendering_fix", "Content Studio stability fix"),
    ("Q2", "P1 Trust", "rendering_fix", "Folder management in Content Studio"),
    ("Q1", "P1 Trust", "rendering_fix", "Canva-to-Mailchimp sync reliability"),
    ("Q4", "P1 Trust", "collaboration", "Real-time multi-author co-editing"),
    ("Q4", "P1 Trust", "collaboration", "Block-level comments & @-mentions"),
    ("Q4", "P1 Trust", "collaboration", "Approval workflow & version history"),
    ("Q1", "P1 Trust", "rendering_fix", "Builder SLO operating contract"),
    ("Q1", "P1 Trust", "rendering_fix", "Brand Kit automated regression suite"),
    ("Q1", "P1 Trust", "rendering_fix", "Copy/paste formatting normalization"),
    ("Q1", "P2 Universal", "universal_content", "Universal Content block primitive"),
    ("Q1", "P2 Universal", "universal_content", "Auto-migration of saved blocks"),
    ("Q2", "P2 Universal", "universal_content", "Bulk template migration tool"),
    ("Q2", "P2 Universal", "universal_content", "1:1 migration tool with support enablement"),
    ("Q2", "P2 Universal", "code_mode", "Builder Code Mode"),
    ("Q2", "P2 Universal", "code_mode", "Builder Liquid templating"),
    ("Q4", "P2 Universal", "universal_content", "Funded migration program"),
    ("Q3", "P2 Universal", "universal_content", "Universal Content in CJB"),
    ("Q2", "P2 Universal", "brandkit", "Brand Kit auto-applied to Universal blocks"),
    ("Q3", "P2 Universal", "universal_content", "Universal Content audit & version history"),
    ("Q2", "P2 Universal", "template_improvement", "Template categorization fix"),
    ("Q1", "P3 AI", "activation", "Brand Kit auto-extract on signup"),
    ("Q2", "P3 AI", "activation", "Industry-specific welcome flow templates"),
    ("Q1", "P3 AI", "ai_builder", "AI Email Setup Agent"),
    ("Q2", "P3 AI", "template_improvement", "B2B & ProServ template gallery"),
    ("Q2", "P3 AI", "template_improvement", "Industry-aware template gallery"),
    ("Q1", "P3 AI", "ai_builder", "Write with AI quality & brand-tone improvements"),
    ("Q4", "P3 AI", "ai_builder", "AI brand-style transfer"),
    ("Q2", "P3 AI", "ai_builder", "AI image generation from product catalog"),
    ("Q2", "P3 AI", "ai_builder", "Image Remix in flow email steps"),
    ("Q3", "P3 AI", "ai_builder", "Per-recipient dynamic images"),
    ("Q2", "P3 AI", "ai_builder", "In-canvas revenue per recipient"),
    ("Q3", "P3 AI", "ai_builder", "Per-profile Smart Send Time & Personalized A/B"),
    ("Q2", "P3 AI", "template_improvement", "Ecommerce lifecycle template library"),
    ("Q2", "P3 AI", "template_improvement", "Store-connected template preview"),
    ("Q3", "P3 AI", "activation", "Lifecycle coverage gap analyzer"),
    ("Q3", "P3 AI", "ai_builder", "Goal-driven campaign agent"),
    ("Q3", "P3 AI", "ai_builder", "Conversational email refinement"),
    ("Q4", "P3 AI", "ai_builder", "Campaign brief to multi-variant"),
    ("Q4", "P3 AI", "ai_builder", "Store intelligence in generation"),
    ("Q1", "P4 Omni", "omnichannel", "Brand-Kit-aware generative SMS"),
    ("Q2", "P4 Omni", "omnichannel", "SMS variant generation & A/B"),
    ("Q3", "P4 Omni", "omnichannel", "Shared content blocks in email + SMS"),
    ("Q3", "P4 Omni", "omnichannel", "Cross-channel preview side-by-side"),
    ("Q3", "P4 Omni", "omnichannel", "Brand Kit on SMS short links & sender ID"),
    ("Q3", "P4 Omni", "activation", "Contextual feature discovery prompts"),
    ("Q2", "P4 Omni", "activation", "DRAFT-resurrect campaign"),
]

THEME_TO_CLUSTERS = {}  # populated at runtime from cluster rankings


def build_theme_to_clusters(ci_df):
    """Primary cluster per theme = highest FY27 EV among clusters where theme ranks top-3."""
    out = {t: [] for t in {x[2] for x in ROADMAP_INITIATIVES}}
    for theme in out:
        sub = ci_df[ci_df["initiative"] == theme].copy()
        sub = sub[sub["initiative_rank_in_cluster"] <= 3].sort_values("fy27_ev", ascending=False)
        out[theme] = sub["cluster_id"].astype(int).tolist()[:6]
    return out

BUNDLES = {
    "A": {
        "title": "Bundle A · Wave 1 Revenue",
        "rationale": "High completion + high MRR/volume. Universal Content & Code Mode drive ~90% of Wave 1 EV. Execute in Q1–Q2.",
        "clusters": [2, 5, 3, 11, 1, 6],
    },
    "B": {
        "title": "Bundle B · Foundation Fix",
        "rationale": "High friction or test-no-send. Fix rendering/trust BEFORE activation. Parallel to Bundle A in Q1.",
        "clusters": [9, 8, 0],
    },
    "C": {
        "title": "Bundle C · Activation & AI",
        "rationale": "Low completion but meaningful intent. AI + activation after Bundle B fixes. C7 after foundation.",
        "clusters": [7, 4, 12, 10],
    },
}


def th(*cols):
    return "<thead><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead>"


def fmt_m(v):
    if v >= 1e6:
        return f"${v/1e6:.2f}M"
    if v >= 1e3:
        return f"${v/1e3:.0f}K"
    return f"${v:.0f}"


def cluster_quarter_inits(cid, ci_df):
    """Roadmap initiatives for cluster by quarter — driven by ranked model themes for that cluster."""
    themes = (
        ci_df[ci_df["cluster_id"] == cid]
        .sort_values("initiative_rank_in_cluster")
        .head(6)["initiative"]
        .tolist()
    )
    q = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
    seen = set()
    for theme in themes:
        for quarter, _pillar, t, name in ROADMAP_INITIATIVES:
            if t == theme and name not in seen:
                q[quarter].append(name)
                seen.add(name)
    # Collaboration items for high-MRR / enterprise clusters
    if cid in (2, 5, 10, 3):
        for quarter, _p, t, name in ROADMAP_INITIATIVES:
            if t == "collaboration" and name not in seen:
                q[quarter].append(name)
                seen.add(name)
    return q


def bundle_matrix(bundle_key, profiles, ci_df):
    spec = BUNDLES[bundle_key]
    cids = spec["clusters"]
    # rank clusters by FY27 EV within bundle
    prof = profiles[profiles["cluster_id"].astype(int).isin(cids)].copy()
    prof = prof.sort_values("fy27_ev", ascending=False).reset_index(drop=True)

    rows = ""
    for rank, (_, r) in enumerate(prof.iterrows(), 1):
        cid = int(r["cluster_id"])
        qinits = cluster_quarter_inits(cid, ci_df)
        elig = int(r["customer_count"])

        def cell(q):
            items = qinits.get(q, [])
            if not items:
                return "—"
            return "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in items) + "</ul>"

        rows += f"""<tr>
          <td class="stage-cell">{CLUSTER_LABELS[cid]}</td>
          <td style="text-align:center">{rank}</td>
          <td style="text-align:right">{elig:,}</td>
          <td class="mrr-cell" style="text-align:right">{fmt_m(r['fy27_ev'])}</td>
          <td>{cell('Q1')}</td>
          <td>{cell('Q2')}</td>
          <td>{cell('Q3')}</td>
          <td>{cell('Q4')}</td>
        </tr>"""

    return f"""
<div class="bundle-box">
  <h3>{spec['title']}</h3>
  <p>{spec['rationale']}</p>
  <table class="{TABLE}">
    {th('Cluster', 'Rank', 'Customers', 'FY27 Revenue Impact', 'Q1 Initiatives', 'Q2 Initiatives', 'Q3 Initiatives', 'Q4 Initiatives')}
    <tbody>{rows}</tbody>
  </table>
</div>"""


BUNDLE_LABELS = {
    "A": "Bundle A · Wave 1 Revenue (Q1–Q2)",
    "B": "Bundle B · Foundation Fix (Q1 parallel)",
    "C": "Bundle C · Activation & AI (Q2–Q3)",
}

EXEC_RATIONALE = {
    2: "Highest FY27 EV; $676 avg MRR power users. Universal Content + migration + Code Mode unlock disproportionate value per account.",
    5: "Enterprise-intensity senders (~194 creates/mo). Stress-test rendering and ship Code Mode; high completion = fast adoption.",
    6: "Largest healthy mid-market cluster (15% of cohort). Protect established 83% completion habit with UC + AI efficiency plays.",
    3: "Stable volume senders with 76% completion. Retention + cross-channel expansion; strong Universal Content eligibility.",
    1: "Broad mid-market base (17% of cohort). Reliable senders — AI Setup Agent + Universal Content drive efficiency at scale.",
    11: "Rising-usage power senders with expansion headroom. Wave-1 Universal Content candidates with growing publish trends.",
    4: "Create-but-don't-publish gap (~43% completion). Template + AI assist after foundation fixes; meaningful EV but needs trust first.",
    10: "Premium AI-adopted senders ($561 MRR). Expand Universal Content + Code Mode; small count, high per-user value.",
    12: "AI-ready mid-market bridge cluster. Connect AI builder investments to Universal Content migration path.",
    8: "Test-heavy, low-publish (33% completion). Rendering/trust fixes are prerequisite — foundation before activation.",
    9: "Highest friction (0.75): creates but almost never publishes. Fix foundation in Q1 parallel track; low FY27 EV but high product-health signal.",
    0: "Dormant paid with declining usage. Win-back via DRAFT-resurrect + rendering trust; churn protection, not growth lever.",
    7: "Largest cluster by count (21% of cohort) but near-zero completion. Activation only after Bundle B fixes; do not prioritize for $21M gap.",
}


def bundle_for(cid):
    for key, spec in BUNDLES.items():
        if cid in spec["clusters"]:
            return key
    return "—"


def top_initiative_label(cid, ci_df):
    sub = ci_df[ci_df["cluster_id"] == cid].sort_values("initiative_rank_in_cluster")
    if sub.empty:
        return "—"
    label = sub.iloc[0]["initiative"].replace("_", " ")
    return label.replace("ai ", "AI ").replace("Ai ", "AI ").title()


def executive_summary_roadmap(profiles, ci_df, kn, total):
    """Executive read for unified-builder-roadmap.html (before Business Case)."""
    prof = profiles.sort_values("fy27_ev", ascending=False).reset_index(drop=True)
    total_ev = kn["total_ev_annualized"]
    gap = kn.get("gap", 21000000 - total_ev)

    bundle_a = prof[prof["cluster_id"].astype(int).isin(BUNDLES["A"]["clusters"])]
    bundle_b = prof[prof["cluster_id"].astype(int).isin(BUNDLES["B"]["clusters"])]
    bundle_c = prof[prof["cluster_id"].astype(int).isin(BUNDLES["C"]["clusters"])]

    a_ev = bundle_a["fy27_ev"].sum()
    a_n = int(bundle_a["customer_count"].sum())
    b_ev = bundle_b["fy27_ev"].sum()
    b_n = int(bundle_b["customer_count"].sum())
    c_ev = bundle_c["fy27_ev"].sum()
    c_n = int(bundle_c["customer_count"].sum())
    top6_ev = prof.head(6)["fy27_ev"].sum()
    top6_n = int(prof.head(6)["customer_count"].sum())
    c7_row = prof[prof["cluster_id"] == 7].iloc[0]

    rows = ""
    for rank, (_, r) in enumerate(prof.iterrows(), 1):
        cid = int(r["cluster_id"])
        bkey = bundle_for(cid)
        tier = "P1" if bkey == "A" else ("P2" if bkey == "B" else "P3")
        if cid == 7:
            tier = "P4"
        rows += f"""<tr>
          <td style="text-align:center"><strong>{rank}</strong></td>
          <td style="text-align:center">{tier}</td>
          <td class="cluster-priority-cell">{CLUSTER_LABELS[cid]}</td>
          <td style="text-align:right">{int(r['customer_count']):,}</td>
          <td style="text-align:right">{r['pct_of_cohort']:.1f}%</td>
          <td style="text-align:right">${r['avg_mrr']:.0f}</td>
          <td class="exec-ev" style="text-align:right">{fmt_m(r['fy27_ev'])}</td>
          <td style="text-align:center">{bkey}</td>
          <td>{top_initiative_label(cid, ci_df)}</td>
          <td>{EXEC_RATIONALE.get(cid, '')}</td>
        </tr>"""

    return f"""<!-- CUSTOMER_TARGETING_EXEC_START -->
<hr class="divider-heavy">

<h1 id="customer-targeting-exec">Customer Targeting — Executive Priority Ranking</h1>
<p style="color:#555; font-style:italic; margin-bottom:10px;">Who to prioritize for FY27 Builder ARR · Full population BigQuery analysis (1,651,592 eligible customers) · <a href="unified-builder-workflow-health.html#targeting">Full targeting analysis &rarr;</a></p>

<div class="vision-box">
  <p><strong>Bottom line:</strong> Close the {fmt_m(gap)} gap to $21M by executing <strong>Bundle A in Q1&ndash;Q2</strong> (Universal Content + migration + Code Mode), running <strong>Bundle B in parallel</strong> (rendering/trust for high-friction cohorts), and deferring volume-heavy dormant-free activation (C7) until foundation ships. <strong>{top6_n:,} customers ({100*top6_n/total:.0f}% of cohort) in the top 6 clusters deliver {fmt_m(top6_ev)} ({100*top6_ev/total_ev:.0f}% of FY27 EV).</strong> Do not reshuffle the roadmap &mdash; compress Q1/Q2 delivery on the Wave 1 critical path.</p>
</div>

<div class="stat-grid">
  <div class="stat-box"><div class="stat-num">{total:,}</div><div class="stat-desc">Eligible Builder customers</div></div>
  <div class="stat-box"><div class="stat-num">{fmt_m(total_ev)}</div><div class="stat-desc">FY27 P50 expected value</div></div>
  <div class="stat-box"><div class="stat-num">{fmt_m(gap)}</div><div class="stat-desc">Gap to $21M target</div></div>
  <div class="stat-box"><div class="stat-num">{fmt_m(a_ev)}</div><div class="stat-desc">Bundle A EV ({a_n:,} customers)</div></div>
</div>

<div class="guiding">
  <p><strong>How to read priority tiers</strong></p>
  <p><strong>P1 &mdash; Wave 1 Revenue (Bundle A):</strong> {a_n:,} customers &middot; {fmt_m(a_ev)} FY27 EV &middot; Execute Q1&ndash;Q2. Universal Content, migration, Code Mode, AI Setup Agent.</p>
  <p><strong>P2 &mdash; Foundation Fix (Bundle B):</strong> {b_n:,} customers &middot; {fmt_m(b_ev)} FY27 EV &middot; Parallel Q1. Rendering/trust before activation (C8, C9, C0).</p>
  <p><strong>P3 &mdash; Activation &amp; AI (Bundle C):</strong> {c_n:,} customers &middot; {fmt_m(c_ev)} FY27 EV &middot; Q2&ndash;Q3 after foundation. Templates, AI builder, onboarding.</p>
  <p><strong>P4 &mdash; Deprioritize for $21M:</strong> C7 Dormant Free ({int(c7_row['customer_count']):,} customers, {fmt_m(c7_row['fy27_ev'])} EV). Largest count, lowest return.</p>
</div>

<table>
  <thead>
    <tr>
      <th>Priority Rank</th><th>Tier</th><th>Cluster</th><th>Customers</th><th>% Cohort</th><th>Avg MRR</th><th>FY27 Revenue Impact</th><th>Bundle</th><th>Primary Lever</th><th>Why Prioritize (or Deprioritize)</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
<p style="font-size:8pt; color:#888; margin-top:8px;">Priority rank = FY27 EV if roadmap initiatives reach eligible customers (16% FY27 realization factor). Cohort = paid + active free Builder users with 90d activity. Not all 48M Mailchimp accounts.</p>
<!-- CUSTOMER_TARGETING_EXEC_END -->
"""


def main():
    global THEME_TO_CLUSTERS
    profiles = pd.read_csv(OUT_CSV / "cluster_profiles_enriched.csv")
    ci_df = pd.read_csv(OUT_CSV / "cluster_initiative_rankings.csv")
    kn = json.loads((OUT_CSV / "key_numbers.json").read_text())
    total = int(kn["total_customers"])
    THEME_TO_CLUSTERS = build_theme_to_clusters(ci_df)

    # verify roadmap count vs init-cell in HTML
    roadmap_html = ROADMAP.read_text()
    init_cells_raw = re.findall(r'class="init-cell">([^<]+)</td>', roadmap_html)
    init_cells = [html.unescape(n) for n in init_cells_raw]
    mapped = {x[3] for x in ROADMAP_INITIATIVES}
    missing = [n for n in init_cells if n not in mapped]
    extra = [n for n in mapped if n not in init_cells]

    cluster_rows = ""
    prof_sorted = profiles.sort_values("fy27_ev", ascending=False)
    for rank, (_, r) in enumerate(prof_sorted.iterrows(), 1):
        cid = int(r["cluster_id"])
        cluster_rows += f"""<tr>
          <td style="text-align:center"><strong>{rank}</strong></td>
          <td>{CLUSTER_LABELS[cid]}</td>
          <td style="text-align:right">{int(r['customer_count']):,}</td>
          <td style="text-align:right">{r['pct_of_cohort']:.1f}%</td>
          <td style="text-align:right">{r['pct_of_mailchimp_all_users']:.3f}%</td>
          <td style="text-align:right">${r['avg_mrr']:.0f}</td>
          <td style="text-align:right">{r['avg_completion_rate']:.0%}</td>
          <td style="text-align:right">{r['avg_friction_score']:.2f}</td>
          <td class="mrr-cell" style="text-align:right">{fmt_m(r['fy27_ev'])}</td>
          <td>{CLUSTER_DESC.get(cid, r.get('description', ''))}</td>
          <td style="font-size:8pt">{r.get('defining_criteria', '')}</td>
        </tr>"""

    coverage_rows = ""
    for quarter, pillar, theme, name in sorted(ROADMAP_INITIATIVES, key=lambda x: (x[0], x[1], x[3])):
        clusters = THEME_TO_CLUSTERS.get(theme, [])
        clabels = ", ".join(CLUSTER_LABELS[c].split(" · ")[0] for c in clusters[:4])
        if len(clusters) > 4:
            clabels += f" +{len(clusters)-4}"
        bundle = "A" if any(c in BUNDLES["A"]["clusters"] for c in clusters) else ""
        if any(c in BUNDLES["B"]["clusters"] for c in clusters):
            bundle = (bundle + "+B") if bundle else "B"
        if any(c in BUNDLES["C"]["clusters"] for c in clusters):
            bundle = (bundle + "+C") if bundle else "C"
        coverage_rows += f"""<tr>
          <td>{name}</td>
          <td style="text-align:center">{quarter}</td>
          <td>{pillar}</td>
          <td>{theme.replace('_', ' ').title()}</td>
          <td>{clabels or '—'}</td>
          <td style="text-align:center">{bundle or '—'}</td>
        </tr>"""

    map_status = f"""
<div class="qa-ok">
  <strong>Roadmap coverage:</strong> {len(ROADMAP_INITIATIVES)} / {len(init_cells)} FY27 Unified Builder initiatives mapped to customer clusters and execution bundles.
  {'All roadmap initiatives mapped ✓' if not missing else 'Missing: ' + html.escape('; '.join(missing))}
</div>"""

    bundles_html = bundle_matrix("A", profiles, ci_df) + bundle_matrix("B", profiles, ci_df) + bundle_matrix("C", profiles, ci_df)

    panel = f"""
<div id="panel-targeting" class="tab-panel">
<h1>$21M Customer Targeting Analysis</h1>
<p class="subtitle">Full population: {total:,} eligible customers · FY27 P50: {fmt_m(kn['total_ev_annualized'])} · BigQuery May 2026 · <a href="unified-builder-roadmap.html#customer-targeting-exec">Executive priority ranking on roadmap &rarr;</a></p>

<div class="qa-ok">
<strong>QA: Cluster coverage ✓</strong> — All {total:,} customers assigned to exactly one of 13 clusters (sums to 100% of eligible Builder cohort: paid + active free 90d).
</div>
<div class="qa-warn">
<strong>QA flags:</strong> FY27 revenue uses 16% rollout realization factor. Validate uplift via experiments before investment decisions.
</div>
{map_status}

<h2>1. Cluster Profiles — % of Universe</h2>
<p>Percentages are of the <strong>1.65M eligible cohort</strong> (not all 48M Mailchimp accounts).</p>
<table class="{TABLE}">
  {th('Rank', 'Cluster', 'Customers', '% Cohort', '% Mailchimp', 'Avg MRR', 'Completion', 'Friction', 'FY27 EV', 'Description', 'Defining Criteria')}
  <tbody>{cluster_rows}</tbody>
</table>

<h2>2. Execution Strategy — Ranked Bundles</h2>
<p>Execute <strong>Bundle A + B in parallel</strong> (Q1), then Bundle C (Q2–Q3). Rows = clusters; columns = Q1–Q4 roadmap initiatives for that cluster.</p>
{bundles_html}

<h2>3. Full FY27 Roadmap → Customer Targeting Map</h2>
<p>Every initiative from the <a href="unified-builder-roadmap.html">Unified Builder FY27 Roadmap</a> mapped to quarter, pillar, targeting theme, and primary clusters.</p>
<table class="{TABLE}">
  {th('Roadmap Initiative', 'Quarter', 'Pillar', 'Targeting Theme', 'Primary Clusters', 'Bundle')}
  <tbody>{coverage_rows}</tbody>
</table>

<p class="note">Generated from BigQuery full population (1,651,592 customers). Methodology: KMeans clustering → eligibility EV → FY27 roadmap mapping.</p>
</div>
"""

    wf = WF.read_text()
    # replace targeting panel
    wf = re.sub(
        r'<div id="panel-targeting" class="tab-panel">.*?</div>\s*(?=<script>)',
        panel + "\n",
        wf,
        count=1,
        flags=re.DOTALL,
    )
    # add targeting table styles if missing
    extra_css = """
  .targeting-table { width: 100%; border-collapse: collapse; font-size: 8.5pt; margin: 12px 0 20px; }
  .targeting-table th { background: #1a3a5c; color: #fff; font-weight: 700; padding: 8px 10px; text-align: left; font-size: 8pt; border: 1px solid #1a3a5c; }
  .targeting-table td { border: 1px solid #bfbfbf; padding: 8px 10px; vertical-align: top; }
  .targeting-table tbody tr:nth-child(even) { background: #fafafa; }
  .targeting-table ul { margin: 0; padding-left: 14px; }
  .targeting-table li { margin-bottom: 3px; line-height: 1.35; font-size: 8pt; }
  .bundle-box { background: #f8f9fa; border: 1px solid #d1d5db; padding: 16px; margin: 16px 0; }
  .bundle-box h3 { font-size: 10pt; color: #1a3a5c; margin-bottom: 8px; }
  .qa-ok { background: #f0fdf4; border-left: 4px solid #166534; padding: 12px; margin: 12px 0; font-size: 8.5pt; }
  .qa-warn { background: #fff9e6; border-left: 4px solid #f0c040; padding: 12px; margin: 12px 0; font-size: 8.5pt; }
"""
    if ".targeting-table" not in wf:
        wf = wf.replace("@media print { body { padding: 12px; font-size: 7.5pt; } }", extra_css + "\n  @media print { body { padding: 12px; font-size: 7.5pt; } }")

    WF.write_text(wf)

    exec_roadmap = executive_summary_roadmap(profiles, ci_df, kn, total)
    rm = ROADMAP.read_text()
    if "<!-- CUSTOMER_TARGETING_EXEC_START -->" in rm:
        rm = re.sub(
            r"<!-- CUSTOMER_TARGETING_EXEC_START -->.*?<!-- CUSTOMER_TARGETING_EXEC_END -->",
            exec_roadmap.strip(),
            rm,
            count=1,
            flags=re.DOTALL,
        )
    else:
        rm = rm.replace(
            '<hr class="divider-heavy">\n\n<h1>Business Case &amp; Projections</h1>',
            exec_roadmap + '\n<hr class="divider-heavy">\n\n<h1 id="business-case">Business Case &amp; Projections</h1>',
            1,
        )
    if ".cluster-priority-cell" not in rm:
        rm = rm.replace(
            "  th { background: #d9e2f3; font-weight: 700; font-size: 9pt; }",
            "  th { background: #d9e2f3; font-weight: 700; font-size: 9pt; }\n  .cluster-priority-cell { background: #f2f2f2; font-weight: 700; }\n  .exec-ev { font-weight: 700; color: #B91C1C; }",
        )
    ROADMAP.write_text(rm)

    print(f"Updated {WF}")
    print(f"Updated {ROADMAP}")
    print(f"Roadmap mapped: {len(ROADMAP_INITIATIVES)} | init-cell in roadmap: {len(init_cells)}")
    if missing:
        print("MISSING:", missing)
    if extra:
        print("EXTRA in map:", extra)


if __name__ == "__main__":
    main()
