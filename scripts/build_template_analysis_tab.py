#!/usr/bin/env python3
"""Generate NUNI Template Analysis tab for unified-builder-workflow-health.html."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "unified-builder-workflow-health.html"
START = "<!-- TEMPLATE_ANALYSIS_START -->"
END = "<!-- TEMPLATE_ANALYSIS_END -->"


def panel() -> str:
    return """
<!-- TEMPLATE_ANALYSIS_START -->
<div id="panel-templates" class="tab-panel">
<h1>NUNI / New Builder Template Analysis</h1>
<p class="subtitle">Production template catalog, paid-customer adoption, 12-month traction, VOC gaps, and competitive template coverage &middot; New Builder (NUNI) scope, excluding NEA/Classic-only layouts &middot; May 2026</p>

<div class="meta-box">
  <div class="meta-item"><strong>Catalog source:</strong> <code>mailchimp.gallery_templates</code> (709 entries) + NUNI runtime catalog (~260+ in <code>nuni-template-sources</code>)</div>
  <div class="meta-item"><strong>Usage source:</strong> <code>bi_activities.users_activities</code> email create/publish events (template property flags)</div>
  <div class="meta-item"><strong>Paid base:</strong> <code>bi_finance.user_cloud_monthly_status</code> (Apr 2026, MRR &gt; 0)</div>
  <div class="meta-item"><strong>VoC:</strong> unitQ (12mo) + Builder Workflow Health themes; Slack HVC channels referenced where aligned</div>
  <div class="meta-item"><strong>Limitation:</strong> Events do not expose per-template IDs at scale &mdash; adoption reported by <em>template type</em> and gallery <em>category</em>, not individual template SKU</div>
</div>

<div class="summary-bar">
  <div class="summary-card"><div class="num">709</div><div class="label">Gallery templates in production catalog</div></div>
  <div class="summary-card"><div class="num">638</div><div class="label">Pre-designed (ready to use)</div></div>
  <div class="summary-card"><div class="num">118</div><div class="label">NUNI-capable (<code>has_neapolitan</code>)</div></div>
  <div class="summary-card"><div class="num">1.06M</div><div class="label">Paid customers (Apr 2026)</div></div>
</div>

<div class="bundle-box">
  <h3>Analysis 1 &mdash; Three synthesis insights (Catalog &amp; lifecycle)</h3>
  <ol style="font-size:9pt;line-height:1.55;margin-left:18px;">
    <li><strong>The catalog is broad but shallow on lifecycle intent.</strong> 709 gallery templates skew seasonal (148), newsletter (96), and vertical d&eacute;cor (Restaurant, Music, Sports) &mdash; not goal-filtered lifecycle kits (welcome, abandoned cart, win-back) the way Klaviyo surfaces 160+ templates by use case.</li>
    <li><strong>NUNI coverage is partial in BQ.</strong> Only 118/709 gallery rows are NUNI-capable; the runtime NUNI JSON catalog (~260+) is the authoritative New Builder set. SMS/WhatsApp do not appear as first-class gallery templates &mdash; email (+ RSS-to-email, Eventbrite) only.</li>
    <li><strong>AutoConnect templates are integration-specific, not vertical lifecycle.</strong> 22 templates (Eventbrite, Facebook Events, SurveyGizmo) solve narrow integration sends; they do not substitute for ecommerce lifecycle or B2B welcome series customers request in VoC.</li>
  </ol>
</div>

<h2>1. Production Template Catalog by Thematic Category</h2>
<p style="font-size:8.5pt;color:#555;margin-bottom:8px;">From <code>mailchimp.gallery_templates</code>. Channel = email unless noted. Lifecycle use case in plain language.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Category</th><th>Count</th><th>What it does (one sentence)</th><th>Lifecycle use case</th><th>Channels</th><th>Example templates</th></tr></thead>
  <tbody>
    <tr><td><strong>Holiday &amp; Seasonal</strong></td><td>148</td><td>Pre-styled layouts for calendar moments (Christmas, Halloween, Valentine&rsquo;s, etc.).</td><td>Seasonal promo bursts &mdash; not ongoing lifecycle.</td><td>Email</td><td>Christmas, Halloween, Valentine&rsquo;s Day, Thanksgiving, New Year</td></tr>
    <tr><td><strong>Newsletters</strong></td><td>96</td><td>Recurring content layouts with hero, columns, and footer patterns.</td><td>Weekly/monthly nurture &mdash; retention, not acquisition.</td><td>Email</td><td>Newsletter variants, mobile-friendly layouts</td></tr>
    <tr><td><strong>E-commerce</strong></td><td>47</td><td>Product-forward layouts for promotions, coupons, and storefront highlights.</td><td>Promo/sale campaigns; partial product showcase &mdash; <em>not</em> full abandoned-cart/checkout lifecycle series.</td><td>Email</td><td>Black Friday Sale, Hero Image, Boutique, Color Box, E-commerce Products</td></tr>
    <tr><td><strong>Sports / Music / Restaurant / Food</strong></td><td>104</td><td>Vertical d&eacute;cor templates matching industry aesthetics.</td><td>Industry-branded broadcasts; weak activation for non-ecom verticals.</td><td>Email</td><td>Restaurant, Music, Hockey/Soccer/Golf sport variants</td></tr>
    <tr><td><strong>Nonprofit / Inspirational / Education</strong></td><td>46</td><td>Mission-driven and community layouts.</td><td>Donor updates, community announcements &mdash; gap vs requested B2B/ProServ welcome flows.</td><td>Email</td><td>Nonprofit, Inspirational, Education, Environment</td></tr>
    <tr><td><strong>Events &amp; AutoConnect</strong></td><td>51</td><td>Event invitations and integration pulls (Eventbrite, Facebook, SurveyGizmo).</td><td>Event promotion &amp; RSVP &mdash; single-send, not multi-step lifecycle.</td><td>Email (+ Eventbrite integration type)</td><td>Eventbrite Multi-Event, Facebook Events, SurveyGizmo Invitation</td></tr>
    <tr><td><strong>Functional / RSS / Reminders</strong></td><td>43</td><td>Utility layouts: RSS-to-email, reminders, notifications, coupons.</td><td>Automated content syndication &amp; transactional-style reminders.</td><td>Email, RSS-to-email</td><td>RSS-To-Email, Reminders, Notifications, Coupons</td></tr>
    <tr><td><strong>Technology / Real Estate / Other verticals</strong></td><td>39</td><td>Smaller vertical slices and general business layouts.</td><td>Prospect nurture for tech/real estate &mdash; under-indexed vs ecom.</td><td>Email</td><td>Technology, Real Estate, Fitness, Beauty</td></tr>
    <tr><td><strong>Snap / legacy / uncategorized</strong></td><td>23</td><td>Legacy or platform-specific shells (many non-predesigned).</td><td>Low activation value; contributes to &ldquo;can&rsquo;t find the right template&rdquo; VoC.</td><td>Email</td><td>Snap (20, mostly non-predesigned)</td></tr>
  </tbody>
</table>

<h2>2. Paid-Customer Adoption by Template Type (Last 12 Months)</h2>
<p style="font-size:8.5pt;color:#555;">Apr 2026 paid base: <strong>1,064,868</strong> customers (988,477 below $299/mo + 76,391 HVC $299+). Property flags on email create/publish events.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Template type</th><th>Customers using (12mo)</th><th>% of paid base</th><th>Human description</th><th>Traction (12mo)</th></tr></thead>
  <tbody>
    <tr><td><strong>Paid gallery template</strong><br><code>uses_paid_template=true</code></td><td>~844,886</td><td><strong>79.3%</strong></td><td>Customer started from a Mailchimp pre-built gallery layout (most common path).</td><td><span style="color:#555;">Flat</span> &mdash; ~1.7&ndash;1.85M distinct users/half-year stable</td></tr>
    <tr><td><strong>Custom / saved template</strong><br><code>uses_custom_template=true</code></td><td>~87,531</td><td><strong>8.2%</strong></td><td>Customer reused their own saved template (power-user / agency behavior).</td><td><span style="color:#166534;">Gaining among HVC</span> &mdash; 17.8% of $299+ vs 7.5% below</td></tr>
    <tr><td><strong>NUNI Creative Assistant template</strong><br><code>is_creative_assistant_template=true</code></td><td>~34,901</td><td><strong>3.3%</strong></td><td>Customer used a New Builder AI/Creative Assistant pre-built design.</td><td><span style="color:#B91C1C;">Losing</span> &mdash; monthly users peaked ~16.3K (Oct 2025), down to ~7.9K (Apr 2026)</td></tr>
    <tr><td><strong>Purchased premium template</strong><br><code>is_purchased_template=true</code></td><td>&lt;500</td><td><strong>&lt;0.05%</strong></td><td>Customer bought a premium marketplace template.</td><td><span style="color:#555;">Negligible</span></td></tr>
  </tbody>
</table>

<div class="bundle-box">
  <h3>Analysis 2 &mdash; Three synthesis insights (Adoption)</h3>
  <ol style="font-size:9pt;line-height:1.55;margin-left:18px;">
    <li><strong>Mailchimp paid customers overwhelmingly use legacy gallery templates (79%), not NUNI CA templates (3.3%).</strong> The New Builder template story is not yet the default activation path for paid senders.</li>
    <li><strong>NUNI CA template usage is in material decline:</strong> H1 CA users fell from 81K to 46K YoY (&minus;44%); H2 from 78K to 22K (&minus;72%). Paid gallery usage stayed flat &mdash; customers aren&rsquo;t leaving templates; they&rsquo;re leaving NUNI CA templates.</li>
    <li><strong>Brand-new paid customers (&le;30 days) show 0% NUNI CA adoption</strong> (617 users, 63% paid gallery, 12% custom). Activation still routes through classic gallery, not AI/NUNI starters.</li>
  </ol>
</div>

<h2>3. Segment Cuts: MRR, Tenure, First 30 Days</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Segment</th><th>Paid customers</th><th>% using paid gallery</th><th>% using custom template</th><th>% using NUNI CA template</th><th>Insight</th></tr></thead>
  <tbody>
    <tr><td><strong>HVC ($299+/mo)</strong></td><td>76,391</td><td>90.9%</td><td>17.8%</td><td>4.3%</td><td>Power users reuse custom templates; still low NUNI CA penetration.</td></tr>
    <tr><td><strong>Below $299/mo</strong></td><td>988,477</td><td>78.5%</td><td>7.5%</td><td>3.2%</td><td>Gallery-dependent; CA templates barely register.</td></tr>
    <tr><td><strong>Tenure &le;90 days (paid)</strong></td><td>23,940</td><td>81.3%</td><td>&mdash;</td><td><strong>0.0%</strong></td><td>New paid accounts never touch NUNI CA templates in year 1.</td></tr>
    <tr><td><strong>Tenure &gt;90 days (paid)</strong></td><td>759,820</td><td>79.1%</td><td>&mdash;</td><td>3.8%</td><td>CA usage concentrates in established accounts, and is falling.</td></tr>
    <tr><td><strong>New paid, first 30 days</strong></td><td>617</td><td>63.4%</td><td>11.5%</td><td>0.0%</td><td>Top early path = paid gallery; CA not in first-send journey.</td></tr>
  </tbody>
</table>
<p class="note">Vertical cuts (E-commerce vs B2B vs ProServ vs Community): onboarding join incomplete in BQ schema this run; roadmap VoC confirms ecommerce-first gallery bias &mdash; B2B/nonprofit &ldquo;no starting point&rdquo; is a documented activation gap. Recommend follow-up join to <code>users_onboarding_responses</code> once question metadata is mapped.</p>

<h2>4. Twelve-Month Traction: Gaining, Flat, Losing</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Template motion</th><th>Metric</th><th>Peak / baseline</th><th>Latest (Apr 2026)</th><th>Verdict</th></tr></thead>
  <tbody>
    <tr><td>NUNI CA template users/mo</td><td>Distinct users</td><td>16,282 (Oct 2025)</td><td>7,951</td><td style="color:#B91C1C;font-weight:700;">Losing (&minus;51% from peak)</td></tr>
    <tr><td>NUNI CA template events/mo</td><td>Create + publish events</td><td>93,012 (Oct 2025)</td><td>66,436</td><td style="color:#B91C1C;font-weight:700;">Losing</td></tr>
    <tr><td>Paid gallery template users</td><td>Distinct users / half-year</td><td>~1.85M</td><td>~1.70M</td><td style="color:#555;font-weight:700;">Flat</td></tr>
    <tr><td>Custom template users (HVC)</td><td>% of $299+ cohort</td><td>&mdash;</td><td>17.8%</td><td style="color:#166534;font-weight:700;">Gaining vs sub-$299 (7.5%)</td></tr>
    <tr><td>New gallery templates added</td><td><code>date_created</code> last 12mo</td><td>0 net new in BQ gallery</td><td>&mdash;</td><td style="color:#555;">Flat catalog; FY27 roadmap adds lifecycle library Q2</td></tr>
  </tbody>
</table>

<h2>5. VoC-Requested Templates We Don&rsquo;t Fully Support Today</h2>
<p style="font-size:8.5pt;color:#555;">From unitQ category <strong>Template Management::Dissatisfaction With Template Quality And Availability</strong> (+167% YoY, 8 items) + Builder Workflow Health themes. Slack HVC (#hvc_feedback, #mc-hvc-escalations) aligns on template findability and portability.</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Requested template / capability</th><th>What it should do</th><th>Source</th><th>In product today?</th></tr></thead>
  <tbody>
    <tr><td><strong>Industry lifecycle series</strong> (welcome &rarr; nurture &rarr; win-back per vertical)</td><td>Pre-built multi-email sequences matched to business type at signup.</td><td>Roadmap VoC; CJB parity gap; unitQ template quality category</td><td style="color:#B91C1C;">No &mdash; single layouts only</td></tr>
    <tr><td><strong>B2B / Professional services gallery</strong></td><td>Skeleton layouts for consultants, agencies, SaaS &mdash; not ecommerce product grids.</td><td>FY27 roadmap (Q2); HeyMarvin UR; Slack HVC</td><td style="color:#B91C1C;">No &mdash; planned Q2</td></tr>
    <tr><td><strong>Ecommerce lifecycle w/ live product blocks</strong></td><td>Abandoned browse/cart/checkout, post-purchase, replenishment with store SKUs populated.</td><td>unitQ; Klaviyo public lifecycle sets; targeting initiative</td><td style="color:#B91C1C;">Partial &mdash; promo layouts exist, not lifecycle series</td></tr>
    <tr><td><strong>Searchable template gallery by goal</strong></td><td>Filter by use case (welcome, promo, abandoned cart) not just category d&eacute;cor.</td><td>Workflow Health Stage 1 VoC; Klaviyo UX benchmark</td><td style="color:#B91C1C;">No</td></tr>
    <tr><td><strong>Save section / campaign as reusable template</strong></td><td>Account-level blocks portable across campaigns (Universal Content).</td><td>Stage 7 VoC (&minus;48 sentiment); Classic migration pain</td><td style="color:#B91C1C;">No &mdash; UC on roadmap Q1&ndash;Q2</td></tr>
    <tr><td><strong>Templates visible in campaign wizard</strong></td><td>New Builder templates appear when creating a campaign.</td><td>nuni-repo HVC #6 ($1,950/mo); unitQ</td><td style="color:#B91C1C;">Bug / gap &mdash; API&harr;wizard contract</td></tr>
    <tr><td><strong>Non-ecom vertical starters</strong> (nonprofit, restaurant beyond d&eacute;cor)</td><td>Goal-specific starters, not just themed shells.</td><td>Onboarding VoC; activation &minus;2.4pp YoY</td><td style="color:#B91C1C;">Weak &mdash; d&eacute;cor-only</td></tr>
  </tbody>
</table>

<div class="bundle-box">
  <h3>Analysis 3 &mdash; Three synthesis insights (VoC &amp; gaps)</h3>
  <ol style="font-size:9pt;line-height:1.55;margin-left:18px;">
    <li><strong>Customers aren&rsquo;t asking for more holiday skins &mdash; they want goal-based lifecycle kits</strong> searchable by job (welcome, abandoned cart, win-back). unitQ template dissatisfaction is up 167% YoY while seasonal catalog is our largest category (148 templates).</li>
    <li><strong>Half the VoC is discoverability and portability, not net-new design.</strong> Templates not in wizard, can&rsquo;t save sections, legacy vs NUNI bifurcation &mdash; fixing surfacing + Universal Content may outperform adding templates.</li>
    <li><strong>Requested templates map directly to FY27 roadmap holes:</strong> B2B/ProServ gallery, ecommerce lifecycle library, store-connected preview &mdash; all Q2, after trust/UC foundation.</li>
  </ol>
</div>

<h2>6. Competitive Template Gap: Klaviyo &amp; Canva (Public Sources)</h2>
<table class="detail-table targeting-table">
  <thead><tr><th>Capability</th><th>Klaviyo (public)</th><th>Canva (public)</th><th>Mailchimp NUNI today</th><th>Gap?</th></tr></thead>
  <tbody>
    <tr><td>Template count / browse</td><td>160+ email templates; filter by goal (welcome, abandoned cart, win-back)</td><td>1,700+ email newsletter templates; vertical browse</td><td>709 gallery; category browse (Holiday, E-com, etc.)</td><td style="color:#B91C1C;">Yes &mdash; goal filter + lifecycle depth</td></tr>
    <tr><td>Lifecycle flow templates</td><td>Welcome, browse/cart/checkout abandon, post-purchase, win-back, sunset</td><td>Design presets; not ESP lifecycle</td><td>Single-send promo/event layouts</td><td style="color:#B91C1C;">Yes vs Klaviyo</td></tr>
    <tr><td>Universal / reusable blocks in templates</td><td>Universal content blocks across templates</td><td>Brand templates; export HTML</td><td>Template-scoped content; UC on roadmap</td><td style="color:#B91C1C;">Yes</td></tr>
    <tr><td>Template folders / organization</td><td>My Templates folders (2025)</td><td>Brand kits + folders</td><td>Limited organization</td><td style="color:#B91C1C;">Yes</td></tr>
    <tr><td>Store-connected product blocks</td><td>Product blocks in templates + flows</td><td>Manual product imagery</td><td>Static product layouts; live store Q2</td><td style="color:#B91C1C;">Yes</td></tr>
    <tr><td>SMS / WhatsApp templates in same gallery</td><td>Multi-channel canvas templates</td><td>Email design export only</td><td>Email-first gallery; SMS separate surface</td><td style="color:#B91C1C;">Yes vs Klaviyo</td></tr>
    <tr><td>Vertical depth (nonprofit, real estate, etc.)</td><td>Ecom + B2C focus</td><td>Strong vertical browse (420K+ total designs)</td><td>Moderate vertical d&eacute;cor categories</td><td style="color:#92400E;">Partial</td></tr>
  </tbody>
</table>

<h2>7. Gap-Closure Impact on Unified Builder Microsegments</h2>
<p style="font-size:8.5pt;color:#555;">If we ship VoC + competitive gap templates (lifecycle library, B2B/ProServ gallery, store-connected preview, wizard surfacing), estimated addressable share from FY27 cluster EV model:</p>
<table class="detail-table targeting-table">
  <thead><tr><th>Proposed template pack</th><th>Primary clusters</th><th>Est. % of pack EV</th><th>Rationale</th></tr></thead>
  <tbody>
    <tr><td>Ecommerce lifecycle library (12 stages)</td><td>C4 Growing-but-Incomplete, C2 High-MRR, C8 High-Friction</td><td><strong>34% + 26% + 8%</strong> of pack EV</td><td>C4 over-indexes on template/initiative EV; completion gap aligns with lifecycle starters.</td></tr>
    <tr><td>Store-connected template preview</td><td>C4, C2, C12 AI-Ready Mid-Market</td><td><strong>~68%</strong> combined</td><td>Store-data-aware generation is top moat; preview closes trust gap for incomplete senders.</td></tr>
    <tr><td>B2B / ProServ skeleton gallery</td><td>C1 Reliable Mid-Market, C11 Rising-Usage, C7 Dormant Free</td><td><strong>11% + 8% + 1%</strong></td><td>Fixes onboarding mismatch; C7 is volume-heavy but low EV &mdash; don&rsquo;t over-invest Q1.</td></tr>
    <tr><td>Wizard surfacing + UC portability fix</td><td>C9 High-Friction, C8, C0 Dormant Paid</td><td><strong>Cross-cutting</strong></td><td>Unblocks existing catalog usage before net-new templates; Bundle B trust prerequisite.</td></tr>
  </tbody>
</table>
<p class="note"><strong>~55&ndash;60% of gap-template EV</strong> concentrates in Bundle A/C clusters (C2, C4, C5, C12) already on the $21M critical path. Closing template gaps is synergistic with Universal Content Q1&ndash;Q2, not a separate track.</p>

<hr style="border:none;border-top:3px solid #1a3a5c;margin:28px 0;">

<h2>Executive Summary &mdash; What You Should Know</h2>
<div class="bundle-box" style="background:#eef2ff;border-color:#1a3a5c;">
  <ol style="font-size:9.5pt;line-height:1.6;margin-left:18px;">
    <li><strong>709 production gallery templates exist, but only 3.3% of paid customers used NUNI CA templates in the last year.</strong> 79% still use classic paid gallery layouts. The New Builder template investment is not yet the default paid experience.</li>
    <li><strong>NUNI CA template usage is declining fast</strong> (&minus;51% from Oct 2025 peak) while paid gallery usage is flat. This is a surfacing/quality problem as much as a catalog size problem.</li>
    <li><strong>The catalog is seasonally deep, lifecycle shallow.</strong> 148 holiday templates vs zero goal-filtered lifecycle series (welcome, abandoned cart/checkout, win-back) that Klaviyo ships publicly.</li>
    <li><strong>VoC + unitQ (+167% template dissatisfaction) asks for goal-based, vertical lifecycle kits and wizard discoverability</strong> &mdash; not more decorative categories. Half the pain is portability (UC) and NUNI/Classic bifurcation.</li>
    <li><strong>Closing the top 5 gaps maps to ~55&ndash;60% of existing Bundle A/C cluster EV</strong> (C2, C4, C5, C12). Template work is on the revenue critical path only when sequenced after Q1 trust + UC primitive.</li>
  </ol>
</div>

<h3>What to do next</h3>
<table class="detail-table targeting-table">
  <thead><tr><th>Priority</th><th>Action</th><th>Owner lane</th><th>Why now</th></tr></thead>
  <tbody>
    <tr><td><strong>P0</strong></td><td>Fix campaign wizard &harr; NUNI API template contract (integration test: create &rarr; visible in wizard in 30s)</td><td>NUNI / nuni-api</td><td>Zero CA adoption in first-30-day paid cohort; HVC escalation pattern</td></tr>
    <tr><td><strong>P0</strong></td><td>Ship Universal Content primitive + migration (Q1&ndash;Q2 roadmap)</td><td>Universal Builder</td><td>VoC #2 theme: templates not portable; unlocks reuse without 181-template rewrites</td></tr>
    <tr><td><strong>P1</strong></td><td>Launch ecommerce lifecycle template library + store-connected preview (Q2)</td><td>AI / Templates</td><td>Closes Klaviyo lifecycle gap; 34% EV to C4 alone</td></tr>
    <tr><td><strong>P1</strong></td><td>Add goal-based gallery filters (welcome / promo / lifecycle / win-back)</td><td>Builder UX</td><td>Matches Klaviyo browse pattern; addresses unitQ +167% dissatisfaction</td></tr>
    <tr><td><strong>P2</strong></td><td>B2B &amp; ProServ skeleton gallery (Q2 roadmap)</td><td>Templates</td><td>Fixes ecommerce-first bias for non-retail onboarding cohorts</td></tr>
    <tr><td><strong>Measure</strong></td><td>Track <code>is_creative_assistant_template</code> adoption monthly; target reverse decline by Q3</td><td>R&amp;A</td><td>Leading indicator that NUNI templates are winning vs flat gallery</td></tr>
  </tbody>
</table>

<p class="note">Analysis generated May 26, 2026. BigQuery pipeline date Apr 2026. Per-template SKU adoption requires event instrumentation (<code>template_id</code> on create) &mdash; recommend PRD add if leadership wants template-level ranking beyond category/type flags.</p>
</div>
<!-- TEMPLATE_ANALYSIS_END -->
"""


def patch_html(content: str) -> str:
    panel_html = panel().strip()
    if START in content and END in content:
        pre, rest = content.split(START, 1)
        _, post = rest.split(END, 1)
        content = pre + panel_html + post
    else:
        anchor = '<script>\nfunction showPageTab'
        if anchor not in content:
            raise SystemExit("Could not find script anchor in HTML")
        content = content.replace(anchor, panel_html + "\n\n" + anchor)

    content = content.replace(
        '  <a href="#targeting" id="tab-link-targeting" onclick="return showPageTab(\'targeting\')">$21M Customer Targeting</a>\n</div>',
        '  <a href="#targeting" id="tab-link-targeting" onclick="return showPageTab(\'targeting\')">$21M Customer Targeting</a>\n'
        '  <a href="#templates" id="tab-link-templates" onclick="return showPageTab(\'templates\')">NUNI Template Analysis</a>\n</div>',
    )

    content = content.replace(
        "  if (hash === 'targeting' || hash === 'workflow') showPageTab(hash);",
        "  if (hash === 'targeting' || hash === 'workflow' || hash === 'templates') showPageTab(hash);",
    )
    content = content.replace(
        "    if (h === 'targeting' || h === 'workflow') showPageTab(h);",
        "    if (h === 'targeting' || h === 'workflow' || h === 'templates') showPageTab(h);",
    )
    return content


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    HTML.write_text(patch_html(text), encoding="utf-8")
    print(f"Updated {HTML}")


if __name__ == "__main__":
    main()
