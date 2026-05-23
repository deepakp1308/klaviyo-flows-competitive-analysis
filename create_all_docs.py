from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_cell_shading(cell, color):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)

def add_cell(cell, text, bold=False, size=9):
    cell.text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = 'Arial'
    run.bold = bold

def make_table(doc, data, header_color='D9E2F3'):
    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(data):
        for j, text in enumerate(row):
            cell = table.cell(i, j)
            add_cell(cell, text, bold=(i==0), size=8)
            if i == 0:
                set_cell_shading(cell, header_color)
    return table

def setup_doc():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)
    for level in range(1, 4):
        h = doc.styles[f'Heading {level}']
        h.font.name = 'Arial'
        h.font.color.rgb = RGBColor(0, 0, 0)
    return doc

# ============================================================
# DOC 2: VP SWIM LANES
# ============================================================
doc = setup_doc()
p = doc.add_paragraph()
run = p.add_run('Unified Builder \u2014 VP Swim Lane Mapping')
run.font.size = Pt(18)
run.bold = True

doc.add_paragraph('52 initiatives from 4 builder strategic pillars mapped to 5 VP-level swim lanes across FY27')

doc.add_heading('Pillar Legend', level=2)
doc.add_paragraph('P1: Builder Trust & Reliability | P2: Universal Builder, Portability & Migration | P3: AI-Powered Builder & Accelerated Time to Value | P4: Unified Omni-Channel Builder & Activation')

swimlanes = [
    ["FY27 Roadmap", "Q1 FY27", "Q2 FY27", "Q3 FY27", "Q4 FY27"],
    ["Accelerate Activation to First Business Payoff",
     "\u2022 Brand Kit auto-extract (P3)\n\u2022 AI Setup Agent STARTS (P3)\n\u2022 Universal Content primitive (P2)\n\u2022 Auto-migration saved blocks (P2)\n\u2022 Bulk migration STARTS (P2)\n\u2022 Write with AI quality (P3)",
     "\u2022 AI Setup Agent SHIPS (P3)\n\u2022 Industry templates (P3)\n\u2022 B2B/ProServ gallery (P3)\n\u2022 Ecommerce lifecycle templates (P3)\n\u2022 Store-connected preview (P3)\n\u2022 Template categorization fix (P2)\n\u2022 Bulk migration SHIPS (P2)",
     "\u2022 Contextual discovery prompts (P4)\n\u2022 DRAFT-resurrect (P4)\n\u2022 UC blocks in CJB (P2)\n\u2022 Lifecycle gap analyzer (P3)",
     "\u2022 Funded migration program (P2)"],
    ["Win ICP Expansion Through Product-Led Growth",
     "\u2022 Builder Code Mode STARTS (P2)",
     "\u2022 Builder Code Mode SHIPS (P2)\n\u2022 Liquid templating (P2)\n\u2022 1:1 migration tool (P2)\n\u2022 In-canvas revenue per recipient (P3)",
     "\u2022 Multi-brand kits (P1)\n\u2022 UC audit & version history (P2)\n\u2022 Smart Send & Personalized A/B (P3)\n\u2022 Per-recipient dynamic images (P3)",
     "\u2022 Real-time co-editing (P1)\n\u2022 Block-level comments (P1)\n\u2022 Approval workflow (P1)\n\u2022 Locked layouts (P1)\n\u2022 Cross-account brand inheritance (P1)\n\u2022 AI brand-style transfer (P3)"],
    ["Scale Omnichannel Adoption",
     "\u2022 Brand-Kit-aware generative SMS (P4)",
     "\u2022 SMS variant gen & A/B (P4)",
     "\u2022 Shared blocks email+SMS (P4)\n\u2022 Cross-channel preview (P4)\n\u2022 Brand Kit on SMS short links (P4)",
     "\u2014"],
    ["Become an AI-First Platform",
     "\u2022 Brand Kit auto-extract (P3)\n\u2022 Write with AI quality (P3)\n\u2022 AI Setup Agent STARTS (P3)\n\u2022 Generative SMS (P4)\n\u2022 Brand voice profile (P1)",
     "\u2022 AI Setup Agent SHIPS (P3)\n\u2022 AI image gen from catalog (P3)\n\u2022 Image Remix (P3)\n\u2022 In-canvas revenue (P3)\n\u2022 SMS variant gen (P4)",
     "\u2022 Per-recipient dynamic images (P3)\n\u2022 Smart Send & A/B (P3)\n\u2022 Goal-driven campaign agent (P3)\n\u2022 Conversational refinement (P3)\n\u2022 Discovery prompts (P4)",
     "\u2022 AI brand-style transfer (P3)\n\u2022 Campaign brief to multi-variant (P3)\n\u2022 Store intelligence in generation (P3)"],
    ["Step Function Quality & Performance",
     "\u2022 Inbox rendering parity (P1)\n\u2022 Block reorder & drag-drop (P1)\n\u2022 Template surfacing (P1)\n\u2022 Cross-browser regression suite (P1)\n\u2022 Save-conflict detection (P1)\n\u2022 Brand Kit correctness (P1)\n\u2022 Font upload parity (P1)\n\u2022 Brand voice profile (P1)\n\u2022 Brand Kit regression suite (P1)\n\u2022 Copy/paste normalization (P1)\n\u2022 Content Studio stability (P1)\n\u2022 Canva sync reliability (P1)\n\u2022 Builder SLO contract (P1)",
     "\u2022 Light/dark mode (P1)\n\u2022 Link checker & deliverability (P1)\n\u2022 Brand fonts in LP/forms (P1)\n\u2022 Folder mgmt Content Studio (P1)\n\u2022 Brand compliance score (P1)\n\u2022 Brand Kit maturity dashboard (P1)",
     "\u2014",
     "\u2014"]
]

doc.add_heading('VP Swim Lane Roadmap', level=1)
make_table(doc, swimlanes, '1A3A5C')
for idx, row in enumerate(doc.tables[-1].rows):
    if idx == 0:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.color.rgb = RGBColor(255, 255, 255)

doc.add_page_break()
doc.add_heading('Mapping Rationale', level=1)

rationale = [
    ("Accelerate Activation to First Business Payoff", "Initiatives that compress time from signup to first send. Brand Kit auto-extract, AI Setup Agent, Universal Content, template improvements, and contextual discovery prompts. The activation gap represents ~$14.3M in unrealized ARR."),
    ("Win ICP Expansion Through Product-Led Growth", "Initiatives that drive upgrades and expansion revenue. Code Mode unlocks Premium/agency users ($1-2M ARR at risk). Multi-brand kits, collaboration, and governance serve the agency and mid-market segments."),
    ("Scale Omnichannel Adoption", "Initiatives that unify email and SMS into one authoring surface. Directly addresses the 0/5 omni-channel score vs Klaviyo's 3."),
    ("Become an AI-First Platform", "Core AI capabilities that transform the builder into an intelligent authoring surface. Builds the compounding creative-performance intelligence loop."),
    ("Step Function Quality & Performance", "All reliability, rendering, and trust initiatives. Addresses ~$15.5K/mo in cited HVC MRR. Concentrated in Q1-Q2 because trust is the foundation.")
]

for title, desc in rationale:
    p = doc.add_paragraph()
    run = p.add_run(f'{title}: ')
    run.bold = True
    run = p.add_run(desc)
    p.style = doc.styles['List Bullet']

doc.save('/Users/dprabhakara/Downloads/FY27_Unified_Builder_VP_Swim_Lanes.docx')
print('VP Swim Lanes doc saved.')

# ============================================================
# DOC 3: CRITICAL PATH & HYPOTHESES
# ============================================================
doc = setup_doc()
p = doc.add_paragraph()
run = p.add_run('Unified Builder \u2014 Critical Path & Hypotheses')
run.font.size = Pt(18)
run.bold = True

doc.add_paragraph('10 highest-leverage initiatives across 4 quarters driving ~65% of the total projected revenue impact (~$13.7M of $21M).')

quarters = [
    ("Q1: Foundation, Trust & AI Quick Wins", [
        ("Inbox Rendering Parity + Builder SLO + Brand Kit Regression Suite",
         "If we fix the top rendering bugs, publish a Builder SLO contract, and ship an automated Brand Kit regression suite, bulk churn will begin reversing from 40.0% and Brand Kit complaints will reverse from their +104% worsening trend.",
         "Emails render differently in inbox. $5,879/mo P0 escalation blocked sends. Brand Kit is the only worsening stage (+104%). ~$15.5K/mo HVC MRR cited.",
         "The email a customer designs is the email every recipient sees. Brand Kit regressions caught pre-release.",
         "Overall CSAT: 3.87 \u2192 4.0. Bulk churn: 40.0% \u2192 39.5%",
         "CSAT recovery is the single largest retention lever. ~$1.0M ARR from churn reduction."),
        ("Universal Content Block Primitive",
         "If we ship Universal Content as an account-level primitive, customers with 10+ templates will adopt it within 60 days.",
         "Saved content is template-scoped. Customer with 181 templates maintains the same footer 181 times. Klaviyo shipped this Spring 2026.",
         "Edit a header or footer once; all sends update automatically.",
         "UC adoption: 0% \u2192 20% of active users within 60 days",
         "Contributes to L1 bulk recovery lever (~$1.9M paid adoption target)."),
        ("Brand Kit Auto-Extract on Signup",
         "If we auto-extract Brand Kit on signup, median time to first send will compress from 6 days toward 4 days.",
         "Customers sign up, get generic templates, must manually restyle. Activation dropped -2.4pp YoY.",
         "First email looks on-brand without any manual restyling.",
         "Time to first send: 6 days \u2192 4 days. Activation: 60.6% \u2192 61.5%",
         "Contributes to the $5.6M trial cohort target.")
    ]),
    ("Q2: AI at Scale & Migration Ships", [
        ("AI Email Setup Agent SHIPS",
         "If a customer can paste a URL and get a scaffolded campaign in 3 clicks, time to first send will compress to under 2 days.",
         "Klaviyo's Marketing Agent sets up flows in ~3 clicks. Mailchimp has no equivalent. Trial activation is 10.8% and dropping.",
         "First campaign is live before onboarding finishes. Matches Klaviyo's speed.",
         "Time to first send: 4 days \u2192 <2 days. Trial activation: 10.8% \u2192 13%",
         "~$2.5M toward the $5.6M trial target."),
        ("Builder Code Mode SHIPS",
         "If we ship Code Mode before Classic sunset, Premium/agency users will migrate voluntarily.",
         "No HTML/CSS escape hatch in Builder. Classic sunset without Code Mode risks $1-2M ARR.",
         "Power users get Builder without giving up control. Safe to retire Classic.",
         "25% voluntary migration within 90 days of GA",
         "Mitigates $1-2M Classic sunset ARR risk.")
    ]),
    ("Q3: Unified Omni-Channel", [
        ("Shared Content Blocks in Email + SMS",
         "If Universal Content extends to SMS, cross-channel campaign creation rate will increase to 15%.",
         "Email and SMS are separate surfaces. 0/5 omni-channel score vs Klaviyo's 3.",
         "Compose once, ship everywhere.",
         "Cross-channel campaign rate: 0% \u2192 15%. SMS attach: 1.5x",
         "Cross-channel users retain at higher rates."),
        ("Per-Profile Smart Send Time & Personalized A/B",
         "If sends ship at per-recipient optimal time, open rates will increase 10-15%.",
         "Klaviyo has all three with 10-30% lift cited. Mailchimp has store-level only.",
         "Sends ship at the per-recipient optimal time.",
         "Open rate: +10-15%. Click rate: +5-8%",
         "Performance lift drives higher MC-attributed revenue."),
        ("Goal-Driven Campaign Agent",
         "If a merchant describes a goal and gets a complete on-brand campaign, creation time drops from ~45 min to <10 min.",
         "No platform generates a complete email from goal + brand + store data. Biggest strategic whitespace.",
         "Describe what you want, get a campaign ready to review. First mover advantage.",
         "Campaign creation: ~45 min \u2192 <10 min. Agent adoption: 20% within 90 days",
         "Faster creation drives repeat rate. Store-data-aware generation improves performance.")
    ]),
    ("Q4: Team Scale & Governance", [
        ("Real-Time Co-Editing + Approval Workflow",
         "If teams can co-edit with comments and approvals, Mailchimp will reverse the -48 net sentiment on collaboration.",
         "Only one person can edit at a time. Save conflicts lose work. Approvals happen outside the product.",
         "Teams work together natively inside Mailchimp with full audit trail.",
         "Collaboration sentiment: -48 \u2192 positive. Multi-author sessions: 20%",
         "Team-account retention lifts. Collaboration justifies Standard/Premium tiers.")
    ])
]

for q_title, bets in quarters:
    doc.add_heading(q_title, level=1)
    for name, hypothesis, problem, benefit, leading, lagging in bets:
        doc.add_heading(name, level=2)
        for label, content in [("Hypothesis", hypothesis), ("Customer Problem", problem), ("Customer Benefit", benefit), ("Leading Indicator", leading), ("Lagging Impact", lagging)]:
            p = doc.add_paragraph()
            run = p.add_run(f'{label}: ')
            run.bold = True
            p.add_run(content)

doc.add_page_break()
doc.add_heading('Cumulative Summary: Critical Path (~65% of Portfolio)', level=1)
p = doc.add_paragraph()
run = p.add_run('Estimated Revenue Impact: ~$13.7M / $21.0M (65%)')
run.bold = True
run.font.size = Pt(14)

doc.save('/Users/dprabhakara/Downloads/FY27_Unified_Builder_Critical_Path.docx')
print('Critical Path doc saved.')

# ============================================================
# DOC 4: REVENUE ATTRIBUTION (summary)
# ============================================================
doc = setup_doc()
p = doc.add_paragraph()
run = p.add_run('Unified Builder \u2014 Initiative Revenue Attribution')
run.font.size = Pt(18)
run.bold = True

doc.add_paragraph('Per-initiative revenue breakdown across retention, trial-to-paid, free-to-paid, and upgrades. Total: ~$21.0M ARR.')

doc.add_heading('Revenue by Channel', level=2)
channel_data = [
    ["Channel", "ARR ($M)", "Share"],
    ["Retention", "$4.0M", "19%"],
    ["Trial-to-Paid", "$5.6M", "27%"],
    ["Free-to-Paid", "$8.7M", "41%"],
    ["Upgrades", "$2.7M", "13%"],
    ["Grand Total", "$21.0M", "100%"]
]
make_table(doc, channel_data)

doc.add_heading('Revenue by Pillar', level=2)
pillar_data = [
    ["Pillar", "Retention", "Trial-to-Paid", "Free-to-Paid", "Upgrades", "Total", "Share"],
    ["P1 \u2014 Quality & Rendering", "$2.20M", "\u2014", "$1.30M", "$0.90M", "$4.40M", "21%"],
    ["P2 \u2014 Brand Kit & Brand Experience", "$0.70M", "$0.80M", "$1.10M", "$0.50M", "$3.10M", "15%"],
    ["P3 \u2014 Templates & Activation", "\u2014", "$3.10M", "$2.75M", "$0.55M", "$6.40M", "30%"],
    ["P4 \u2014 Content Reuse & Discovery", "$0.90M", "$0.60M", "$1.55M", "$0.55M", "$3.60M", "17%"],
    ["P5 \u2014 AI & Campaign Intelligence", "$0.20M", "$1.10M", "$2.00M", "$0.20M", "$3.50M", "17%"],
    ["Grand Total", "$4.00M", "$5.60M", "$8.70M", "$2.70M", "$21.00M", "100%"]
]
make_table(doc, pillar_data)

doc.add_heading('Methodology & Assumptions', level=2)
doc.add_paragraph('Data Sources: bi_aggregate.product_journey_monthly, bi_aggregate.mbr_monthly. ARPU at-booking: $45.35/mo ($540/yr), steady-state: $91.44/mo ($1,097/yr). Volume: 1,015,648 paid active users/mo, 870,303 free, ~2.36M trial signups/yr.')
doc.add_paragraph('Conservative Guardrails: Editor causal shares: 50% paid adoption, 35% paid repeat, 30% paid CSAT, 20% free, 25% trial. No compounding. All conversion uses at-booking ARPU.')
doc.add_paragraph('Key Risks: CSAT is largest paid contributor ($3.1M of $6.7M). Free cohort depends on activation recovery. Trial depends on time-to-first-send compression. Attribution requires controlled experimentation.')

doc.save('/Users/dprabhakara/Downloads/FY27_Unified_Builder_Revenue_Attribution.docx')
print('Revenue Attribution doc saved.')

# ============================================================
# DOC 5: WORKFLOW HEALTH & VOC
# ============================================================
doc = setup_doc()
p = doc.add_paragraph()
run = p.add_run('Unified Builder \u2014 Workflow Health & VOC')
run.font.size = Pt(18)
run.bold = True

doc.add_paragraph('Customer-reported bugs and barriers mapped to 7 email builder workflow stages, with MRR exposure and top cited issues.')
doc.add_paragraph('Data Window: Feb 22 \u2013 May 22, 2026 (last 3 months) | Source: unitQ | Channels: Zendesk, in-app feedback, CSAT/PRS surveys | Filters: Negative sentiment, quality_issue + experience_issue')

doc.add_heading('Summary', level=2)
doc.add_paragraph('Combined MRR Exposure: $149K+/mo | Total Negative VOC: 2,056 items | Bug MRR: $77K/mo | Barrier MRR: $73K/mo')

doc.add_heading('MRR Exposure by Workflow Stage', level=1)
stage_data = [
    ["Workflow Stage", "JTBD", "Combined MRR", "VOC Items", "Top Bugs", "Top Barriers"],
    ["1. Choose Structure", "Define the Skeleton", "$15.7K/mo", "731", "Builder hides forms/analytics; confusing navigation", "Template library hard to find; only legacy templates show"],
    ["2. Establish Brand & Style", "Set the Rules", "$12.1K/mo", "194", "Font uploads fail; logo previews broken; dark mode errors", "Brand Kit styles revert; no centralized propagation"],
    ["3. Add & Place Content", "Assemble", "$3.7K/mo", "304", "Drag-drop reorders after save; copy/paste breaks layout", "Blocks unclickable; images vanish; no reusable block library"],
    ["4. Refine & Polish", "Craft", "$9.7K/mo", "308", "Text formatting drifts; Word paste breaks styles", "Rigid templates; no clean HTML; limited formatting tools"],
    ["5. Personalize & Tailor", "Add Context", "$38.3K/mo", "110", "Merge tags blank; segment logic overlaps; save failures", "Audience confusing; tags desync; automations skip sends"],
    ["6. Preview & Validate", "Gain Confidence", "$60.7K/mo", "351", "Preview differs from Outlook/mobile; test emails bounce", "Mobile toggle merges desktop edits; preview grayed out"],
    ["7. Learn + Reuse", "Be Efficient", "$11.6K/mo", "58", "Duplicating campaigns corrupts layout", "Can't save as template; no cross-campaign block library"]
]
make_table(doc, stage_data)

doc.add_page_break()
doc.add_heading('Trend: Are We Getting Better or Worse?', level=1)
doc.add_paragraph('Comparing Jul\u2013Oct 2025 (baseline) vs Feb\u2013May 2026 (current):')

trend_data = [
    ["Workflow Stage", "Jul-Oct 2025", "Feb-May 2026", "Change", "Trend"],
    ["1. Choose Structure", "795", "569", "-28.4%", "Improving"],
    ["2. Establish Brand & Style", "52", "106", "+103.8%", "WORSENING"],
    ["3. Add & Place Content", "96", "81", "-15.6%", "Improving"],
    ["4. Refine & Polish", "149", "131", "-12.1%", "Flat"],
    ["5. Personalize & Tailor", "121", "99", "-18.2%", "Improving"],
    ["6. Preview & Validate", "278", "159", "-42.8%", "Improving"],
    ["7. Learn + Reuse", "14", "12", "-14.3%", "Flat"]
]
make_table(doc, trend_data)

doc.add_paragraph('')
p = doc.add_paragraph()
run = p.add_run('Action Required: ')
run.bold = True
p.add_run('Establish Brand & Style is the only worsening stage (+104%). Brand Kit font uploads, logo previews, and style propagation are regressing while every other stage is improving or flat. This directly blocks the "AI That Knows Your Brand" tenet. The Q1 Brand Kit regression suite is urgent.')

doc.save('/Users/dprabhakara/Downloads/FY27_Unified_Builder_Workflow_Health.docx')
print('Workflow Health doc saved.')

print('\nAll 4 additional docs created successfully!')
