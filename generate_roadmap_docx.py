#!/usr/bin/env python3
"""Generate FY27 Unified Builder Strategy Roadmap Word document."""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

OUTPUT_PATH = "/Users/dprabhakara/Downloads/FY27_Unified_Builder_Strategy_Roadmap.docx"

doc = Document()

# ---------------------------------------------------------------------------
# Global style configuration
# ---------------------------------------------------------------------------
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.space_before = Pt(0)
style.paragraph_format.line_spacing = 1.15

for level in range(1, 4):
    hs = doc.styles[f'Heading {level}']
    hs.font.name = 'Calibri'
    hs.font.color.rgb = RGBColor(0, 0, 0)
    if level == 1:
        hs.font.size = Pt(20)
        hs.paragraph_format.space_before = Pt(12)
        hs.paragraph_format.space_after = Pt(6)
    elif level == 2:
        hs.font.size = Pt(14)
        hs.paragraph_format.space_before = Pt(14)
        hs.paragraph_format.space_after = Pt(6)
    else:
        hs.font.size = Pt(12)
        hs.paragraph_format.space_before = Pt(10)
        hs.paragraph_format.space_after = Pt(4)

list_style = doc.styles['List Bullet']
list_style.font.name = 'Calibri'
list_style.font.size = Pt(11)


def set_cell_shading(cell, color_hex):
    """Apply background shading to a table cell."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def set_cell_text(cell, text, bold=False, size=Pt(9), color=None, alignment=None):
    """Set cell text with formatting."""
    cell.text = ""
    p = cell.paragraphs[0]
    if alignment:
        p.alignment = alignment
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = size
    run.bold = bold
    if color:
        run.font.color.rgb = color
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)


def add_bullet_to_cell(cell, text, bold_prefix=None, size=Pt(9)):
    """Add a bullet point paragraph to a cell."""
    p = cell.add_paragraph()
    p.style = doc.styles['Normal']
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.left_indent = Pt(12)

    pPr = p._p.get_or_add_pPr()
    numPr = parse_xml(
        f'<w:numPr {nsdecls("w")}>'
        f'  <w:ilvl w:val="0"/>'
        f'  <w:numId w:val="1"/>'
        f'</w:numPr>'
    )

    if bold_prefix:
        run_b = p.add_run(bold_prefix)
        run_b.font.name = 'Calibri'
        run_b.font.size = size
        run_b.bold = True
        run_t = p.add_run(text)
        run_t.font.name = 'Calibri'
        run_t.font.size = size
    else:
        run_t = p.add_run(f"\u2022 {text}")
        run_t.font.name = 'Calibri'
        run_t.font.size = size


def add_sub_label_to_cell(cell, text, size=Pt(8)):
    """Add a sub-label (section header) to a cell."""
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run(text.upper())
    run.font.name = 'Calibri'
    run.font.size = size
    run.bold = True
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def format_table(table, header_color="D9E2F3"):
    """Apply consistent formatting to a table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    for cell in table.rows[0].cells:
        set_cell_shading(cell, header_color)
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if header_color == "1A3A5C" else RGBColor(0, 0, 0)


def add_bold_run(paragraph, text):
    run = paragraph.add_run(text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    return run


def add_normal_run(paragraph, text):
    run = paragraph.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    return run


# ===========================================================================
# PAGE 1-2: STRATEGY OVERVIEW
# ===========================================================================

doc.add_heading('Mailchimp Unified Builder', level=1)
subtitle = doc.add_paragraph('FY27 Strategy & Roadmap')
subtitle.runs[0].font.size = Pt(14)
subtitle.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
subtitle.runs[0].font.name = 'Calibri'

# --- Vision ---
doc.add_heading('Vision', level=2)
vision = doc.add_paragraph()
vision.paragraph_format.left_indent = Pt(12)
vision_text = (
    "We envision a future where Mailchimp is the marketing surface that knows your brand, your store, "
    "and your performance history — and turns a business goal into a complete, on-brand campaign ready to send. "
    "Every campaign makes the next one smarter, faster, and more profitable. Leaving Mailchimp doesn't just "
    "mean losing a builder; it means losing compounding marketing intelligence no design tool or ESP can replicate."
)
run = vision.add_run(vision_text)
run.font.name = 'Calibri'
run.font.size = Pt(11)
run.italic = True

# --- The Stubborn Customer Problem ---
doc.add_heading('The Stubborn Customer Problem', level=2)
intro = doc.add_paragraph(
    "Mailchimp customers face four interconnected builder challenges that erode trust, slow activation, "
    "and block the unified authoring experience. Backed by ~$15.5K/mo in builder-related HVC MRR exposure "
    "(Feb\u2013May 2026), 14,000+ VoC reviews, and 25 user research briefs:"
)
intro.runs[0].font.size = Pt(10)
intro.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)

problems = [
    (
        "1. Customers Can\u2019t Trust the Builder They Already Use \u2014 ",
        "~$15.5K/mo in builder-related HVC MRR has been cited in the last 3 months alone. A $5,879/mo P0 "
        "escalation (elDiario.es) blocked campaign sends entirely due to a segmentation bug. A $402/mo customer "
        "reports Builder emails \u201clook totally different when forwarded.\u201d A $3,000/mo Premium customer "
        "writes \u201cbugs cause frustration quite frequently.\u201d Brand Kit serves stale colors after a "
        "partially-ramped fix. Canva graphics vanish from sent emails. Bulk email churn rose +2.1pp YoY to "
        "40%. The builder scores 2 out of 5 on workflow efficiency vs Klaviyo\u2019s 3 and Canva\u2019s 5."
    ),
    (
        "2. Multiple Builders with No Portability or Interoperability \u2014 ",
        "Two parallel builders (New Builder and Classic) share nothing. Templates don\u2019t port. Saved content "
        "is template-scoped, not account-level. Builder bifurcation is the most-cited UX complaint at \u221272 "
        "net sentiment; templates-not-portable at \u221268. A $330/mo customer with 181 templates: \u201cI need "
        "to individually update them which will take days.\u201d A $504/mo customer\u2019s migration support "
        "chat was ended and then abandoned. Retiring Classic without Code Mode risks $1\u20132M in ARR. Klaviyo "
        "shipped Universal Content as the default primitive in Spring 2026. Bulk Established users fell \u22129.4% "
        "YoY, losing ~92K users."
    ),
    (
        "3. Too Many Barriers Between Signup and First Send \u2014 ",
        "Bulk activation dropped \u22122.4pp YoY to 60.6%. Median time to first send is 6 days; user research "
        "shows under 30 minutes is achievable. The <12-month cohort dropped \u221222.8% YoY. Barriers compound: "
        "no Brand Kit auto-extract on signup, an ecommerce-first template gallery that leaves B2B and nonprofits "
        "without a starting point, Write with AI geo-gated to 4 countries (Explore \u221273.7%, churn 77.2%), "
        "and feature discovery gaps measured in years. The Free tier lost ~74K Established users (\u221219.2% "
        "YoY). 30-day repeat send volume dropped \u221228.8%. The activation gap represents ~$14.3M in "
        "unrealized ARR across Free and Trial cohorts."
    ),
    (
        "4. Lack of a Unified Authoring Experience \u2014 ",
        "Email and SMS compose in separate surfaces with no shared content blocks, no shared preview, and no "
        "cross-channel reuse. The builder scores 0 out of 5 on omni-channel capability vs Klaviyo\u2019s 3. "
        "Real-time collaboration doesn\u2019t exist; only one person can edit at a time (\u221248 net sentiment, "
        "second-most-cited user research bet). A $57K/mo HVC customer described their approval workflow: "
        "\u201cI don\u2019t look at it; I just hope it\u2019s right.\u201d Teams needing multi-author workflows, "
        "approval chains, or cross-channel reuse are forced outside the product entirely."
    ),
]

for heading_text, body_text in problems:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    run_h = p.add_run(heading_text)
    run_h.bold = True
    run_h.font.name = 'Calibri'
    run_h.font.size = Pt(11)
    run_b = p.add_run(body_text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(11)

# --- Key Tenets ---
doc.add_heading('Key Tenets: Differentiated Experience & Capability', level=2)

tenets = [
    (
        "1. Trust Before Features \u2014 ",
        "Every send matches the editor. Brand Kit is always current and actively enforced, not just stored. "
        "A compliance score checks every email against brand standards before send. No new capability ships "
        "to production without meeting published SLOs. Reliability is not a prerequisite to check off; it is "
        "the product experience."
    ),
    (
        "2. Author Once, Deliver Everywhere \u2014 ",
        "Content blocks, brand assets, and styles are account-level primitives that propagate across templates, "
        "campaigns, automations, and channels. A footer edited once updates everywhere it appears. No customer "
        "should maintain the same content in two places."
    ),
    (
        "3. AI That Knows Your Brand and Your Store \u2014 ",
        "Every AI capability is grounded in Brand Kit (voice, tone, colors, fonts) and the customer\u2019s store "
        "data (bestsellers, segments, purchase frequency, AOV). AI does not generate generic content; it generates "
        "the customer\u2019s content using the customer\u2019s data. A merchant describes a goal in natural "
        "language and gets a complete, on-brand, store-data-populated campaign ready to review."
    ),
    (
        "4. One Surface, Every Channel \u2014 ",
        "Email, SMS, and future channels compose in one canvas with shared content blocks, side-by-side preview, "
        "and unified reporting. Cross-channel is how the product works, not a separate surface or a billing upgrade."
    ),
    (
        "5. Built for Teams, Not Just Solo Operators \u2014 ",
        "Real-time co-editing, block-level comments, approval workflows, and multi-brand governance scale the "
        "builder from one-person shops to agency teams managing dozens of brands. Collaboration happens inside "
        "the product, not in Slack threads and screenshot approvals."
    ),
]

for heading_text, body_text in tenets:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run_h = p.add_run(heading_text)
    run_h.bold = True
    run_h.font.name = 'Calibri'
    run_h.font.size = Pt(11)
    run_b = p.add_run(body_text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(11)

# --- Customer Benefits ---
doc.add_heading('Customer Benefits', level=2)

benefits = [
    (
        "1. Compress Campaign Creation From Hours to Minutes",
        "AI auto-extracts brand assets on signup, scaffolds campaigns from a URL, and generates on-brand copy "
        "and images in seconds. Universal Content eliminates duplicate maintenance across templates and channels. "
        "The time from blank page to live campaign collapses from days to minutes, giving marketers back the hours "
        "they currently spend on manual restyling, copy-pasting across surfaces, and hunting for assets."
    ),
    (
        "2. Consistent, Configurable, and Collaborative by Default",
        "Brand Kit enforces consistency across every email, SMS, landing page, and AI-generated design without "
        "manual intervention. Multi-brand kits, locked layouts, and role-based governance make the builder "
        "configurable for agencies and multi-brand teams. Real-time co-editing, block-level comments, and "
        "approval workflows bring collaboration inside the product."
    ),
    (
        "3. Higher-Performing Omni-Channel Campaigns Shipped with Confidence",
        "Per-profile Smart Send Time, Personalized A/B, and in-canvas revenue metrics turn the builder from a "
        "composition tool into a performance engine. Cross-channel preview, shared content blocks, and unified "
        "authoring mean email and SMS ship as one coordinated campaign. Published SLOs, rendering fidelity "
        "guarantees, and pre-send quality checks give marketers the confidence to hit send knowing what they "
        "designed is what their customer will receive."
    ),
]

for heading_text, body_text in benefits:
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_after = Pt(2)
    run = p_h.add_run(heading_text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(12)

    p_b = doc.add_paragraph(body_text)
    p_b.runs[0].font.name = 'Calibri'
    p_b.runs[0].font.size = Pt(11)
    p_b.paragraph_format.space_after = Pt(8)

# --- Competitive Moat ---
doc.add_heading('Competitive Moat', level=2)

moats = [
    (
        "Brand & Store-Aware AI That No Design Tool Can Match",
        "Design-first tools can generate layouts, but they don\u2019t know the customer\u2019s audience, send "
        "history, product catalog, or campaign performance. Standalone ESPs have performance data but no creative "
        "intelligence or brand enforcement. Mailchimp\u2019s AI is grounded in Brand Kit (voice, tone, fonts, "
        "colors, logos), the customer\u2019s store data (bestsellers, segments, AOV), and campaign performance "
        "history. A merchant describes a goal and gets a complete, on-brand, store-data-populated campaign. "
        "No competitor ships this combination."
    ),
    (
        "Compounding Creative-Performance Intelligence Loop",
        "Every campaign a customer sends feeds back into the system. Which subject line drove revenue. Which "
        "hero image converted. Which send time worked for which segment. Over time, the builder doesn\u2019t "
        "just help customers create faster; it helps them create better, because creative decisions are informed "
        "by performance data, store intelligence informs product selection, and the lifecycle gap analyzer "
        "proactively surfaces the next highest-ROI email to build. No competitor closes this loop."
    ),
    (
        "Omni-Channel Authoring with Unified Content Primitives",
        "Competing ESPs support multiple channels but author them in separate surfaces with separate content "
        "models. Design tools create beautiful assets but have no send infrastructure. Mailchimp\u2019s Universal "
        "Content primitive renders across email, SMS, and future channels from a single block, with "
        "content-type-aware formatting. One content model, one brand system, one preview surface, one send."
    ),
]

for heading_text, body_text in moats:
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_after = Pt(2)
    run = p_h.add_run(heading_text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(12)

    p_b = doc.add_paragraph(body_text)
    p_b.runs[0].font.name = 'Calibri'
    p_b.runs[0].font.size = Pt(11)
    p_b.paragraph_format.space_after = Pt(8)

# --- How We Measure Success ---
doc.add_heading('How We Measure Success', level=2)

metrics_sections = [
    (
        "Product Adoption, Engagement & Time to Activation",
        "Builder adoption rate across all users from 84% to >90%. Builder activation rate (touched \u2192 "
        "Established) from 55% to >65%. 30-day repeat send rate from 83% to >87%. Universal Content adoption "
        "among Builder active users to 50\u201370% within 6 months of launch. Time to first send from 6 days "
        "median to <2 days. Time from blank page to campaign-ready email from ~45 minutes to <15 minutes."
    ),
    (
        "Customer Benefit Metrics",
        "Average open rate from 28.3% to 35%. Average click rate from 1.7% to 3.0%. Average conversion "
        "(revenue per 1K delivered) from $1.74 to $2.50 (+44%). Mailchimp-attributed revenue as a share of "
        "customer total from ~15% to 25%. Campaign creation time reduced through AI-assisted authoring, "
        "Universal Content reuse, and cross-channel unified workflows."
    ),
    (
        "Business Outcome Metrics",
        "Combined editor-attributed ARR target: ~$21M across adoption, activation, retention, and CSAT levers. "
        "Bulk Established users from 889K to 915\u2013935K/mo. Bulk churn from 40.0% to 36.5\u201337.5%. "
        "SMS attach rate 2\u00d7 baseline. Free-to-paid 90-day conversion rate recovery from 12.6% toward "
        "14.5%. Trial activation (first send within 90 days) from 10.8% to 16%."
    ),
    (
        "Quality Indicators",
        "Builder SLO compliance: uptime \u226599.9%, crash-free sessions \u226599.5%, save/publish reliability "
        "\u226599.99%, rendering fidelity \u226599% across supported email clients. Initial load P95 <500ms. "
        "Overall CSAT from 3.87 toward 4.2/5, Ease of Use CSAT from 3.53 toward 4.0/5, Site Performance "
        "CSAT from 3.86 toward 4.2/5. AI output quality: hallucination rate <1%, brand-tone match rate "
        "measured via Brand Kit grounding score. Cross-browser regression catch rate >95% pre-release."
    ),
]

for heading_text, body_text in metrics_sections:
    p_h = doc.add_paragraph()
    p_h.paragraph_format.space_after = Pt(2)
    run = p_h.add_run(heading_text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(12)

    p_b = doc.add_paragraph(body_text)
    p_b.runs[0].font.name = 'Calibri'
    p_b.runs[0].font.size = Pt(11)
    p_b.paragraph_format.space_after = Pt(8)


# ===========================================================================
# PAGE BREAK -> PAGE 3-4: FY27 PHASED ROADMAP
# ===========================================================================
doc.add_page_break()

doc.add_heading('FY27 Phased Roadmap', level=1)
p_sub = doc.add_paragraph(
    '4 pillars, 4 quarters \u2014 from foundation and AI quick wins to a unified, collaborative omni-channel builder'
)
p_sub.runs[0].font.size = Pt(10)
p_sub.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
p_sub.runs[0].italic = True

# Create roadmap table
roadmap = doc.add_table(rows=5, cols=5)
roadmap.autofit = True

headers = [
    "Strategic Pillar",
    "Q1\nFoundation, Trust & AI Quick Wins",
    "Q2\nAI at Scale & Migration Ships",
    "Q3\nUnified Omni-Channel",
    "Q4\nTeam Scale & Governance",
]
for i, h in enumerate(headers):
    cell = roadmap.rows[0].cells[i]
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(h)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0, 0, 0)
    set_cell_shading(cell, "D9E2F3")

# --- Pillar 1: Builder Trust & Reliability ---
row = roadmap.rows[1]
c0 = row.cells[0]
c0.text = ""
set_cell_shading(c0, "F2F2F2")
p = c0.paragraphs[0]
run = p.add_run("Builder Trust & Reliability")
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(9)
p2 = c0.add_paragraph()
run2 = p2.add_run("Editor rendering, Brand Kit, Content Studio, Canva, platform SLOs, collaboration, governance")
run2.font.name = 'Calibri'
run2.font.size = Pt(7)
run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
run2.italic = True

# Q1
c1 = row.cells[1]
c1.text = ""
for label, items in [
    ("EDITOR RENDERING", [
        "Fix inbox rendering divergence (forwarded-mail reflow, mobile line-breaks, image-shrink)",
        "Fix block reorder, drag-and-drop reliability across devices (incl. iPad/tablet)",
        "Surface Builder templates in campaign creation wizard",
        "Automated cross-browser regression suite",
        "Multi-author save-conflict detection with presence indicators",
    ]),
    ("BRAND KIT", [
        "Brand Kit data correctness fix & drift monitoring (ramp to 100%)",
        "Font upload bug fix & Creative Assistant custom font recognition",
        "Brand voice profile in Brand Kit (tone, vocabulary, CTA styles)",
        "Brand Kit automated regression suite",
    ]),
    ("EDITOR RELIABILITY", [
        "Copy/paste formatting normalization (Word, Google Docs, external sources)",
    ]),
    ("CONTENT STUDIO & CANVA", [
        "Content Studio stability (eliminate quit-and-reload pattern)",
        "Canva-to-Mailchimp sync reliability with sync-status indicators",
    ]),
    ("PLATFORM", [
        "Builder SLO operating contract (99.9% uptime, P95 load <500ms, render fidelity \u226599%)",
    ]),
]:
    add_sub_label_to_cell(c1, label)
    for item in items:
        add_bullet_to_cell(c1, item, size=Pt(8))

# Q2
c2 = row.cells[2]
c2.text = ""
for label, items in [
    ("EDITOR RENDERING", [
        "Light/dark mode variant rendering & background images on blocks",
        "Inline link validation, spam-score guidance & SPF/DKIM/DMARC wizard",
    ]),
    ("BRAND KIT", [
        "Brand fonts selectable in landing pages & signup forms (iPhone fallback fix)",
        "Brand compliance score (0\u2013100 pre-send check against Brand Kit standards)",
        "Brand Kit maturity dashboard (completeness %, guided setup prompts)",
    ]),
    ("CONTENT STUDIO", [
        "Folder reordering, deletion & search-in-folder for asset organization",
    ]),
]:
    add_sub_label_to_cell(c2, label)
    for item in items:
        add_bullet_to_cell(c2, item, size=Pt(8))

# Q3
c3 = row.cells[3]
c3.text = ""
add_sub_label_to_cell(c3, "BRAND KIT")
add_bullet_to_cell(c3, "Multi-brand kits per account (main brand + sub-brands, Canva-style)", size=Pt(8))

# Q4
c4 = row.cells[4]
c4.text = ""
for label, items in [
    ("COLLABORATION", [
        "Real-time multi-author co-editing with live cursors & presence indicators",
        "Block-level @-mention comments with resolve-in-context",
        "Multi-step approval workflow with full version history & rollback",
    ]),
    ("GOVERNANCE", [
        "Locked layouts mode with role-based access for brand governance",
        "Cross-account brand inheritance for agencies (Slack-style context switching)",
    ]),
]:
    add_sub_label_to_cell(c4, label)
    for item in items:
        add_bullet_to_cell(c4, item, size=Pt(8))


# --- Pillar 2: Universal Builder, Portability & Migration ---
row = roadmap.rows[2]
c0 = row.cells[0]
c0.text = ""
set_cell_shading(c0, "F2F2F2")
p = c0.paragraphs[0]
run = p.add_run("Universal Builder, Portability & Migration")
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(9)
p2 = c0.add_paragraph()
run2 = p2.add_run("Universal Content, Classic\u2192Builder migration, cross-product template portability, Code Mode")
run2.font.name = 'Calibri'
run2.font.size = Pt(7)
run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
run2.italic = True

# Q1
c1 = row.cells[1]
c1.text = ""
for label, items in [
    ("UNIVERSAL CONTENT", [
        "Universal Content block primitive (account-level, edit-once-propagates-everywhere)",
        "Auto-migration of existing saved blocks to Universal Content",
    ]),
    ("MIGRATION", [
        "Bulk template migration tool (181-template pattern) STARTS",
        "Builder Code Mode (HTML/CSS escape hatch) STARTS",
    ]),
]:
    add_sub_label_to_cell(c1, label)
    for item in items:
        add_bullet_to_cell(c1, item, size=Pt(8))

# Q2
c2 = row.cells[2]
c2.text = ""
for label, items in [
    ("MIGRATION", [
        "Bulk template migration tool SHIPS",
        "1:1 migration tool with style-fidelity guarantee & support enablement",
        "Builder Code Mode SHIPS (precondition for Classic sunset)",
        "Builder Liquid templating for power users & dynamic content",
    ]),
    ("PORTABILITY", [
        "Brand Kit auto-applied to Universal blocks at insertion",
        "Template categorization fix (layout-only browse mode, better search & tagging)",
    ]),
]:
    add_sub_label_to_cell(c2, label)
    for item in items:
        add_bullet_to_cell(c2, item, size=Pt(8))

# Q3
c3 = row.cells[3]
c3.text = ""
add_sub_label_to_cell(c3, "PORTABILITY")
add_bullet_to_cell(c3, "Universal Content blocks render in Customer Journey Builder email steps", size=Pt(8))
add_bullet_to_cell(c3, "Universal Content audit & version history (impact preview before edit)", size=Pt(8))

# Q4
c4 = row.cells[4]
c4.text = ""
add_sub_label_to_cell(c4, "MIGRATION")
add_bullet_to_cell(c4, "Funded migration program with 12-month grace period & in-product tracker", size=Pt(8))


# --- Pillar 3: AI-Powered Builder ---
row = roadmap.rows[3]
c0 = row.cells[0]
c0.text = ""
set_cell_shading(c0, "F2F2F2")
p = c0.paragraphs[0]
run = p.add_run("AI-Powered Builder & Accelerated Time to Value")
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(9)
p2 = c0.add_paragraph()
run2 = p2.add_run("Activation, onboarding, AI content & copy, AI design, personalization, performance intelligence")
run2.font.name = 'Calibri'
run2.font.size = Pt(7)
run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
run2.italic = True

# Q1
c1 = row.cells[1]
c1.text = ""
for label, items in [
    ("ACTIVATION & ONBOARDING", [
        "Brand Kit auto-extract on signup with first email pre-branded",
        "AI Email Setup Agent (URL \u2192 scaffolded campaign in 3 clicks) STARTS",
    ]),
    ("AI CONTENT", [
        "Write with AI quality & brand-tone improvements (deeper Brand Kit integration)",
    ]),
]:
    add_sub_label_to_cell(c1, label)
    for item in items:
        add_bullet_to_cell(c1, item, size=Pt(8))

# Q2
c2 = row.cells[2]
c2.text = ""
for label, items in [
    ("ACTIVATION & ONBOARDING", [
        "Industry-specific welcome flow templates pre-loaded by business type",
        "AI Email Setup Agent SHIPS",
    ]),
    ("TEMPLATES", [
        "B2B & professional services template gallery (skeleton layouts)",
        "Industry-aware template gallery (6\u20138 per vertical)",
        "Ecommerce lifecycle template library (12 stages \u00d7 3\u20135 variants with live product blocks)",
        "Store-connected template preview (preview with actual products, brand colors, logo)",
    ]),
    ("AI DESIGN & PERFORMANCE", [
        "AI image generation tied to customer product catalog",
        "Image Remix in flow email steps (Klaviyo parity)",
        "In-canvas revenue per recipient & per step (Klaviyo parity)",
    ]),
]:
    add_sub_label_to_cell(c2, label)
    for item in items:
        add_bullet_to_cell(c2, item, size=Pt(8))

# Q3
c3 = row.cells[3]
c3.text = ""
add_sub_label_to_cell(c3, "AI DESIGN & PERSONALIZATION")
for item in [
    "Per-recipient dynamic images (last product viewed, predicted next product)",
    "Per-profile Smart Send Time & Personalized A/B in send config",
    "Lifecycle coverage gap analyzer (\u201cYou're missing winback \u2014 merchants with winback see 12% higher repeat purchase\u201d)",
    "Goal-driven campaign agent (natural language goal \u2192 agent asks questions \u2192 generates complete on-brand email)",
    "Conversational email refinement (iterate in natural language on a live preview)",
]:
    add_bullet_to_cell(c3, item, size=Pt(8))

# Q4
c4 = row.cells[4]
c4.text = ""
add_sub_label_to_cell(c4, "AI CONTENT")
for item in [
    "AI brand-style transfer between campaigns (no competitor ships this)",
    "Campaign brief to multi-variant (goal brief \u2192 3 variants with A/B recommendation)",
    "Store intelligence in generation (AI uses bestsellers, segments, AOV to make content decisions)",
]:
    add_bullet_to_cell(c4, item, size=Pt(8))


# --- Pillar 4: Unified Omni-Channel ---
row = roadmap.rows[4]
c0 = row.cells[0]
c0.text = ""
set_cell_shading(c0, "F2F2F2")
p = c0.paragraphs[0]
run = p.add_run("Unified Omni-Channel Builder & Activation")
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(9)
p2 = c0.add_paragraph()
run2 = p2.add_run("Generative SMS, unified email+SMS authoring, cross-channel preview, feature discovery, activation")
run2.font.name = 'Calibri'
run2.font.size = Pt(7)
run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
run2.italic = True

# Q1
c1 = row.cells[1]
c1.text = ""
add_sub_label_to_cell(c1, "GENERATIVE SMS")
add_bullet_to_cell(c1, "Brand-Kit-aware generative SMS in composer (character-limit auto-compression, brand-tone)", size=Pt(8))

# Q2
c2 = row.cells[2]
c2.text = ""
add_sub_label_to_cell(c2, "GENERATIVE SMS")
add_bullet_to_cell(c2, "SMS variant generation & A/B testing in composer", size=Pt(8))
add_sub_label_to_cell(c2, "ACTIVATION")
add_bullet_to_cell(c2, "DRAFT-resurrect campaign with proactive nudges (\u201cin DRAFT for X days\u201d)", size=Pt(8))

# Q3
c3 = row.cells[3]
c3.text = ""
add_sub_label_to_cell(c3, "UNIFIED AUTHORING")
for item in [
    "Shared content blocks render in both email + SMS (Universal Content extends to SMS)",
    "Cross-channel preview side-by-side at compose time",
    "Brand Kit applied to SMS branded short links & sender ID",
]:
    add_bullet_to_cell(c3, item, size=Pt(8))
add_sub_label_to_cell(c3, "ACTIVATION")
add_bullet_to_cell(c3, "Contextual feature discovery prompts (\u201cturn this into an automation?\u201d)", size=Pt(8))

# Q4
c4 = row.cells[4]
c4.text = ""
p = c4.paragraphs[0]
run = p.add_run("\u2014")
run.font.name = 'Calibri'
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

format_table(roadmap, header_color="D9E2F3")


# ===========================================================================
# PAGE BREAK -> PAGE 4-5: BUSINESS CASE & PROJECTIONS
# ===========================================================================
doc.add_page_break()

doc.add_heading('Business Case & Projections', level=1)
p_sub = doc.add_paragraph(
    'FY26 baseline \u2192 FY27 targets. Editor-attributed ARR model across paid, free, and trial '
    'cohorts using conservative causal shares.'
)
p_sub.runs[0].font.size = Pt(10)
p_sub.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
p_sub.runs[0].italic = True
p_src = doc.add_paragraph(
    'Sources: bi_aggregate.product_journey_monthly, bi_aggregate.mbr_monthly. Pipeline date 2026-05-11.'
)
p_src.runs[0].font.size = Pt(8)
p_src.runs[0].font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# --- FY26 Baselines ---
doc.add_heading('FY26 Baselines', level=2)

baselines = doc.add_table(rows=9, cols=4)
baselines.autofit = True

for i, h in enumerate(["Metric", "Value", "Metric", "Value"]):
    cell = baselines.rows[0].cells[i]
    set_cell_text(cell, h, bold=True, size=Pt(9))
    set_cell_shading(cell, "D9E2F3")

baseline_data = [
    ("Paid Active Users/mo", "1,015,648", "Free Active Users/mo", "870,303"),
    ("Bulk Established/mo", "888,706", "Free Established/mo", "313,806"),
    ("Bulk Adoption Rate", "92.7%", "Free Bulk Adoption", "75.0%"),
    ("Bulk Activation Rate", "60.6%", "Free Bulk Activation", "48.1%"),
    ("30-Day Repeat Send Rate", "83.2%", "Bulk Churn", "40.0% (+2.1pp YoY)"),
    ("Overall CSAT (email builder)", "3.87/5 (73.2% Good+)", "Trial Activation (first send 90d)", "10.8%"),
    ("Median Days to First Send", "5\u20136 days", "ARPU (steady-state)", "$91.44/mo ($1,097/yr)"),
    ("Free \u2192 Paid Conversion (90d)", "12.64%", "Trial Signups/yr", "~2.36M"),
]

for r_idx, (m1, v1, m2, v2) in enumerate(baseline_data, start=1):
    row = baselines.rows[r_idx]
    set_cell_text(row.cells[0], m1, bold=True, size=Pt(9))
    set_cell_text(row.cells[1], v1, size=Pt(9))
    set_cell_text(row.cells[2], m2, bold=True, size=Pt(9))
    set_cell_text(row.cells[3], v2, size=Pt(9))

format_table(baselines)

# --- Leading Indicators ---
doc.add_heading('Leading Indicators: Baselines & Targets', level=2)

li_table = doc.add_table(rows=8, cols=5)
li_table.autofit = True

for i, h in enumerate(["Leading Indicator", "FY26 Baseline", "FY27 Target", "Lift", "What This Measures"]):
    cell = li_table.rows[0].cells[i]
    set_cell_text(cell, h, bold=True, size=Pt(9))
    set_cell_shading(cell, "D9E2F3")

li_data = [
    ("Builder Adoption", "92.7% (paid) / 75.0% (free)", "95% / 82%", "+2.3pp / +7.0pp",
     "% of active users who touch the builder each month."),
    ("Builder Activation", "60.6% (paid) / 48.1% (free)", "67% / 55%", "+6.4pp / +6.9pp",
     "% of users who touch the builder and reach Established status."),
    ("30-Day Repeat Send Rate", "83.2% (paid) / 73.4% (free)", "87% / 80%", "+3.8pp / +6.6pp",
     "% of first-senders who send again within 30 days. Measures stickiness."),
    ("Overall CSAT", "3.87/5 (73.2% Good+)", "4.2/5 (85% Good+)", "+0.33 avg / +11.8pp Good+",
     "Overall satisfaction for email builder users. Dissatisfied users churn at 3\u20135x the rate."),
    ("Ease of Use CSAT", "3.53/5 (54% Easy+)", "4.0/5 (70% Easy+)", "+0.47 avg / +16pp Easy+",
     "Weakest CSAT dimension. Directly impacted by activation friction, template gaps, and AI quality."),
    ("Site Performance CSAT", "3.86/5 (72.9% Good+)", "4.2/5 (85% Good+)", "+0.34 avg / +12.1pp Good+",
     "Rendering bugs, Content Studio crashes, and Canva sync failures drag this score."),
    ("Trial Activation", "10.8%", "16%", "+5.2pp",
     "% of trial signups who send their first email within 90 days."),
]

for r_idx, (ind, base, target, lift, desc) in enumerate(li_data, start=1):
    row = li_table.rows[r_idx]
    set_cell_text(row.cells[0], ind, bold=True, size=Pt(9))
    set_cell_text(row.cells[1], base, size=Pt(9))
    set_cell_text(row.cells[2], target, size=Pt(9))
    set_cell_text(row.cells[3], lift, bold=True, size=Pt(9))
    set_cell_text(row.cells[4], desc, size=Pt(8))

format_table(li_table)

# --- How Leading Indicators Drive Business Outcomes ---
doc.add_heading('How Leading Indicators Drive Business Outcomes', level=2)
p_desc = doc.add_paragraph(
    "Each leading indicator improvement translates to retention, conversion, and upgrade outcomes "
    "through editor-attributed causal shares."
)
p_desc.runs[0].font.size = Pt(10)
p_desc.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)

lid_table = doc.add_table(rows=4, cols=5)
lid_table.autofit = True

for i, h in enumerate([
    "Leading Indicator Lift", "\u2192 Retention (Churn Reduction)",
    "\u2192 Trial-to-Paid", "\u2192 Free-to-Paid", "\u2192 Upgrade Moments"
]):
    cell = lid_table.rows[0].cells[i]
    set_cell_text(cell, h, bold=True, size=Pt(8))
    set_cell_shading(cell, "D9E2F3")

lid_data = [
    (
        "Adoption & Activation",
        "More users reaching Established status = fewer who abandon before experiencing value. Editor causal share: 50% (paid), 20% (free).",
        "Trial users who reach first send within 90 days convert at higher rates. +5.2pp activation = ~123K incremental first-senders/yr.",
        "Free users who activate and repeat-send hit plan limits faster. +6.9pp free activation = ~45K more Established free users.",
        "Activated users who outgrow Free/Essentials encounter upgrade prompts at natural limit-hit moments.",
    ),
    (
        "30-Day Repeat",
        "Repeat senders have proven the platform works for them. +3.8pp paid repeat rate = ~4.8K incremental repeat senders/mo.",
        "Trial users who send a second campaign within 30 days have 2\u20133x higher conversion rates.",
        "Free repeat senders are the highest-propensity free-to-paid segment.",
        "Repeat senders grow contact lists and campaign volume, triggering tier upgrades.",
    ),
    (
        "CSAT Recovery (Overall + Ease of Use + Performance)",
        "Largest single retention contributor. Moving Overall from 3.87 to 4.2, Ease of Use from 3.53 to 4.0, and Performance from 3.86 to 4.2 reduces churn-from-dissatisfaction. Dissatisfied users churn at 3\u20135x the rate.",
        "\u2014",
        "\u2014",
        "\u2014",
    ),
]

for r_idx, (ind, ret, trial, free, upgrade) in enumerate(lid_data, start=1):
    row = lid_table.rows[r_idx]
    set_cell_text(row.cells[0], ind, bold=True, size=Pt(8))
    set_cell_text(row.cells[1], ret, size=Pt(8))
    set_cell_text(row.cells[2], trial, size=Pt(8))
    set_cell_text(row.cells[3], free, size=Pt(8))
    set_cell_text(row.cells[4], upgrade, size=Pt(8))

format_table(lid_table)

# --- Projected Business Impact ---
doc.add_heading('Projected Business Impact', level=2)

proj_table = doc.add_table(rows=4, cols=4)
proj_table.autofit = True

for i, h in enumerate(["Cohort", "Key Levers", "How It Translates", "Editor-Attributed ARR"]):
    cell = proj_table.rows[0].cells[i]
    set_cell_text(cell, h, bold=True, size=Pt(9))
    set_cell_shading(cell, "D9E2F3")

proj_data = [
    (
        "Paid Cohort",
        "Adoption (+2.3pp), Activation (+6.4pp), 30-day repeat (+3.8pp), CSAT recovery (Overall 3.87\u21924.2, Ease of Use 3.53\u21924.0)",
        "23K more adopters, 60K reaching Established, 4.8K more repeat senders, churn reduction from CSAT recovery. Editor causal share: 30\u201350%.",
        "$6.7M",
    ),
    (
        "Free Cohort",
        "Adoption (+7.0pp), Activation (+6.9pp), 30-day repeat (+6.6pp), CSAT recovery",
        "~45K more Established free users. Higher free-to-paid conversion rate recovering from 12.6% toward 14.5%. Editor causal share: 20%.",
        "$8.7M",
    ),
    (
        "Trial Cohort",
        "Trial activation (+5.2pp), 30-day repeat (+7.2pp)",
        "~123K incremental first-senders/yr from trial signups. Trial-to-paid conversion recovering toward 16%. Editor causal share: 25%.",
        "$5.6M",
    ),
]

for r_idx, (cohort, levers, how, arr) in enumerate(proj_data, start=1):
    row = proj_table.rows[r_idx]
    set_cell_text(row.cells[0], cohort, bold=True, size=Pt(9))
    set_cell_text(row.cells[1], levers, size=Pt(9))
    set_cell_text(row.cells[2], how, size=Pt(9))
    set_cell_text(row.cells[3], arr, bold=True, size=Pt(10))

format_table(proj_table)

# --- Total Revenue Impact Box ---
doc.add_paragraph()  # spacer

total_box = doc.add_table(rows=1, cols=1)
total_box.alignment = WD_TABLE_ALIGNMENT.CENTER
cell = total_box.rows[0].cells[0]
cell.text = ""
set_cell_shading(cell, "F5F5F5")

# Add border
tbl = total_box._tbl
tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
borders = parse_xml(
    f'<w:tblBorders {nsdecls("w")}>'
    f'  <w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
    f'  <w:left w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
    f'  <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
    f'  <w:right w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
    f'</w:tblBorders>'
)
tblPr.append(borders)

p_title = cell.paragraphs[0]
run = p_title.add_run("Total Editor-Attributed Annual Revenue Impact")
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(14)

p_total = cell.add_paragraph()
run = p_total.add_run("~$21.0M")
run.bold = True
run.font.name = 'Calibri'
run.font.size = Pt(22)
run2 = p_total.add_run("  Combined ARR across paid, free, and trial cohorts")
run2.font.name = 'Calibri'
run2.font.size = Pt(10)
run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

breakdown = [
    ("$6.7M", "From Paid Cohort: adoption, activation, repeat send, and CSAT-driven retention (32%)"),
    ("$8.7M", "From Free Cohort: free-to-paid conversion uplift through activation and repeat send (41%)"),
    ("$5.6M", "From Trial Cohort: trial-to-paid conversion through faster time to first send (27%)"),
]
for amount, desc in breakdown:
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run_a = p.add_run(amount)
    run_a.bold = True
    run_a.font.name = 'Calibri'
    run_a.font.size = Pt(12)
    run_d = p.add_run(f"  {desc}")
    run_d.font.name = 'Calibri'
    run_d.font.size = Pt(9)
    run_d.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

# --- Methodology & Assumptions ---
doc.add_heading('Methodology & Assumptions', level=2)

method_items = [
    (
        "Data Sources: ",
        "User and adoption baselines from bi_aggregate.product_journey_monthly (89.7M rows, May 2024\u2013Apr 2026). "
        "ARPU from bi_aggregate.mbr_monthly: at-booking $45.35/mo ($540/yr), steady-state $91.44/mo ($1,097/yr). "
        "Volume base: 1,015,648 paid active users/mo, 870,303 free active users/mo, ~2.36M trial signups/yr."
    ),
    (
        "Conservative Guardrails: ",
        "Editor causal shares are conservative: 50% for paid adoption/activation, 35% for paid repeat, "
        "30% for paid CSAT, 20% for free, 25% for trial. CSAT target is 0 (not +30). No compounding assumed. "
        "All conversion estimates use at-booking ARPU ($540/yr), not steady-state ($1,097/yr)."
    ),
    (
        "Key Risks: ",
        "CSAT is the largest single paid-cohort contributor ($3.1M of $6.7M). If quality initiatives slip, "
        "nearly half the paid case weakens. Free cohort ($8.7M) depends on activation recovery and free-to-paid "
        "conversion improving by +1.77pp. Trial cohort ($5.6M) depends on time-to-first-send compressing from "
        "6 days to <2 days. Attribution requires controlled experimentation to validate causal shares."
    ),
]

for heading_text, body_text in method_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run_h = p.add_run(heading_text)
    run_h.bold = True
    run_h.font.name = 'Calibri'
    run_h.font.size = Pt(11)
    run_b = p.add_run(body_text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(11)


# --- Footer ---
doc.add_paragraph()
footer = doc.add_paragraph(
    "Generated from Initiative Canvas v2.0 and Revised Goals \u00b7 52 initiatives across 4 pillars \u00b7 "
    "Source: Editor + SMS competitive analysis, HVC Risk Map, User Research, Product Health, Growth Model, "
    "Strategy 6-Pager"
)
footer.runs[0].font.size = Pt(8)
footer.runs[0].font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ===========================================================================
# Save
# ===========================================================================
doc.save(OUTPUT_PATH)
print(f"Document saved to {OUTPUT_PATH}")
print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")
