from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(11)

for level in range(1, 4):
    h = doc.styles[f'Heading {level}']
    h.font.name = 'Arial'
    h.font.color.rgb = RGBColor(0, 0, 0)

def set_cell_shading(cell, color):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)

def add_table_cell_text(cell, text, bold=False, size=9):
    cell.text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = 'Arial'
    run.bold = bold

# ============ TITLE ============
p = doc.add_paragraph()
run = p.add_run('Mailchimp Unified Builder')
run.font.size = Pt(20)
run.bold = True
run.font.name = 'Arial'

# ============ VISION ============
doc.add_heading('Vision', level=1)
doc.add_paragraph(
    'We envision a future where Mailchimp is the marketing surface that knows your brand, your store, '
    'and your performance history — and turns a business goal into a complete, on-brand campaign ready to send. '
    'Every campaign makes the next one smarter, faster, and more profitable. Leaving Mailchimp doesn\'t just '
    'mean losing a builder; it means losing compounding marketing intelligence no design tool or ESP can replicate.'
)

# ============ STUBBORN CUSTOMER PROBLEM ============
doc.add_heading('The Stubborn Customer Problem', level=1)
doc.add_paragraph(
    'Mailchimp customers face four interconnected builder challenges that erode trust, slow activation, '
    'and block the unified authoring experience. Backed by ~$15.5K/mo in builder-related HVC MRR exposure '
    '(Feb\u2013May 2026), 14,000+ VoC reviews, and 25 user research briefs:'
)

problems = [
    ("Customers Can\u2019t Trust the Builder They Already Use",
     "~$15.5K/mo in builder-related HVC MRR has been cited in the last 3 months alone. A $5,879/mo P0 escalation "
     "(elDiario.es) blocked campaign sends entirely due to a segmentation bug. A $402/mo customer reports emails "
     "\u201clook totally different when forwarded.\u201d A $3,000/mo Premium customer writes \u201cbugs cause "
     "frustration quite frequently.\u201d Brand Kit serves stale colors after a partially-ramped fix. Canva graphics "
     "vanish from sent emails. Bulk email churn rose +2.1pp YoY to 40%. The builder scores 2 out of 5 on workflow "
     "efficiency vs Klaviyo\u2019s 3 and Canva\u2019s 5."),
    ("Multiple Builders with No Portability or Interoperability",
     "Two parallel builders (New Builder and Classic) share nothing. Templates don\u2019t port. Saved content is "
     "template-scoped, not account-level. Builder bifurcation is the most-cited UX complaint at \u221272 net sentiment; "
     "templates-not-portable at \u221268. A $330/mo customer with 181 templates: \u201cI need to individually update "
     "them which will take days.\u201d A $504/mo customer\u2019s migration support chat was ended and then abandoned. "
     "Retiring Classic without Code Mode risks $1\u20132M in ARR. Klaviyo shipped Universal Content as the default "
     "primitive in Spring 2026. Bulk Established users fell \u22129.4% YoY, losing ~92K users."),
    ("Too Many Barriers Between Signup and First Send",
     "Bulk activation dropped \u22122.4pp YoY to 60.6%. Median time to first send is 6 days; user research shows "
     "under 30 minutes is achievable. The <12-month cohort dropped \u221222.8% YoY. Barriers compound: no Brand Kit "
     "auto-extract on signup, an ecommerce-first template gallery that leaves B2B and nonprofits without a starting "
     "point, Write with AI geo-gated to 4 countries (Explore \u221273.7%, churn 77.2%), and feature discovery gaps "
     "measured in years. The Free tier lost ~74K Established users (\u221219.2% YoY). 30-day repeat send volume "
     "dropped \u221228.8%. The activation gap represents ~$14.3M in unrealized ARR across Free and Trial cohorts."),
    ("Lack of a Unified Authoring Experience",
     "Email and SMS compose in separate surfaces with no shared content blocks, no shared preview, and no "
     "cross-channel reuse. The builder scores 0 out of 5 on omni-channel capability vs Klaviyo\u2019s 3. Real-time "
     "collaboration doesn\u2019t exist; only one person can edit at a time (\u221248 net sentiment, second-most-cited "
     "user research bet). A $57K/mo HVC customer described their approval workflow: \u201cI don\u2019t look at it; I "
     "just hope it\u2019s right.\u201d Teams needing multi-author workflows, approval chains, or cross-channel reuse "
     "are forced outside the product entirely.")
]

for title, desc in problems:
    p = doc.add_paragraph()
    run = p.add_run(f'{title}: ')
    run.bold = True
    run.font.size = Pt(11)
    run = p.add_run(desc)
    run.font.size = Pt(11)
    p.style = doc.styles['List Bullet']

# ============ KEY TENETS ============
doc.add_heading('Key Tenets: Differentiated Experience & Capability', level=1)

tenets = [
    ("Trust Before Features", "Every send matches the editor. Brand Kit is always current and actively enforced, not just stored. A compliance score checks every email against brand standards before send. No new capability ships to production without meeting published SLOs."),
    ("Author Once, Deliver Everywhere", "Content blocks, brand assets, and styles are account-level primitives that propagate across templates, campaigns, automations, and channels. A footer edited once updates everywhere it appears."),
    ("AI That Knows Your Brand and Your Store", "Every AI capability is grounded in Brand Kit (voice, tone, colors, fonts) and the customer\u2019s store data (bestsellers, segments, purchase frequency, AOV). A merchant describes a goal in natural language and gets a complete, on-brand, store-data-populated campaign ready to review."),
    ("One Surface, Every Channel", "Email, SMS, and future channels compose in one canvas with shared content blocks, side-by-side preview, and unified reporting. Cross-channel is how the product works, not a separate surface or a billing upgrade."),
    ("Built for Teams, Not Just Solo Operators", "Real-time co-editing, block-level comments, approval workflows, and multi-brand governance scale the builder from one-person shops to agency teams managing dozens of brands.")
]

for title, desc in tenets:
    p = doc.add_paragraph()
    run = p.add_run(f'{title}: ')
    run.bold = True
    run = p.add_run(desc)
    p.style = doc.styles['List Bullet']

# ============ CUSTOMER BENEFITS ============
doc.add_heading('Customer Benefits', level=1)

benefits = [
    ("Compress Campaign Creation From Hours to Minutes", "AI auto-extracts brand assets on signup, scaffolds campaigns from a URL, and generates on-brand copy and images in seconds. Universal Content eliminates duplicate maintenance across templates and channels."),
    ("Consistent, Configurable, and Collaborative by Default", "Brand Kit enforces consistency across every email, SMS, landing page, and AI-generated design without manual intervention. Multi-brand kits, locked layouts, and role-based governance make the builder configurable for agencies and multi-brand teams."),
    ("Higher-Performing Omni-Channel Campaigns Shipped with Confidence", "Per-profile Smart Send Time, Personalized A/B, and in-canvas revenue metrics turn the builder from a composition tool into a performance engine. Published SLOs, rendering fidelity guarantees, and pre-send quality checks give marketers confidence.")
]

for i, (title, desc) in enumerate(benefits, 1):
    p = doc.add_paragraph()
    run = p.add_run(f'{i}. {title}: ')
    run.bold = True
    run = p.add_run(desc)

# ============ COMPETITIVE MOAT ============
doc.add_heading('Competitive Moat', level=1)

moats = [
    ("Brand & Store-Aware AI That No Design Tool Can Match", "Design-first tools can generate layouts, but they don\u2019t know the customer\u2019s audience, send history, product catalog, or campaign performance. Mailchimp\u2019s AI is grounded in Brand Kit AND the customer\u2019s store data. A merchant describes a goal and gets a complete, on-brand, store-data-populated campaign."),
    ("Compounding Creative-Performance Intelligence Loop", "Every campaign feeds back into the system. Which subject line drove revenue. Which hero image converted. Which send time worked for which segment. Over time, the builder helps customers create better, because creative decisions are informed by performance data and store intelligence."),
    ("Omni-Channel Authoring with Unified Content Primitives", "Mailchimp\u2019s Universal Content primitive renders across email, SMS, and future channels from a single block, with content-type-aware formatting. One content model, one brand system, one preview surface, one send.")
]

for title, desc in moats:
    p = doc.add_paragraph()
    run = p.add_run(f'{title}: ')
    run.bold = True
    run = p.add_run(desc)
    p.style = doc.styles['List Bullet']

# ============ HOW WE MEASURE SUCCESS ============
doc.add_heading('How We Measure Success', level=1)

metrics = [
    ("Product Adoption, Engagement & Time to Activation", "Builder adoption rate across all users from 84% to >90%. Builder activation rate from 55% to >65%. 30-day repeat send rate from 83% to >87%. Time to first send from 6 days median to <2 days. Time from blank page to campaign-ready email from ~45 minutes to <15 minutes."),
    ("Customer Benefit Metrics", "Average open rate from 28.3% to 35%. Average click rate from 1.7% to 3.0%. Average conversion (revenue per 1K delivered) from $1.74 to $2.50 (+44%). Mailchimp-attributed revenue as a share of customer total from ~15% to 25%."),
    ("Business Outcome Metrics", "Combined editor-attributed ARR target: ~$21M across adoption, activation, retention, and CSAT levers. Bulk Established users from 889K to 915\u2013935K/mo. Bulk churn from 40.0% to 36.5\u201337.5%. Free-to-paid 90-day conversion rate recovery from 12.6% toward 14.5%. Trial activation from 10.8% to 16%."),
    ("Quality Indicators", "Builder SLO compliance: uptime \u226599.9%, crash-free \u226599.5%, rendering fidelity \u226599%. Overall CSAT from 3.87 toward 4.2/5, Ease of Use CSAT from 3.53 toward 4.0/5, Site Performance CSAT from 3.86 toward 4.2/5. AI hallucination rate <1%. Cross-browser regression catch rate >95% pre-release.")
]

for title, desc in metrics:
    p = doc.add_paragraph()
    run = p.add_run(f'{title}: ')
    run.bold = True
    run = p.add_run(desc)
    p.style = doc.styles['List Bullet']

# ============ PAGE BREAK + ROADMAP TABLE ============
doc.add_page_break()
doc.add_heading('FY27 Phased Roadmap', level=1)

roadmap_data = [
    ["Strategic Pillar", "Q1\nFoundation, Trust & AI Quick Wins", "Q2\nAI at Scale & Migration Ships", "Q3\nUnified Omni-Channel", "Q4\nTeam Scale & Governance"],
    ["Builder Trust & Reliability",
     "\u2022 Fix inbox rendering divergence\n\u2022 Fix block reorder & drag-and-drop (incl. iPad)\n\u2022 Surface Builder templates in wizard\n\u2022 Cross-browser regression suite\n\u2022 Multi-author save-conflict detection\n\u2022 Brand Kit data correctness fix\n\u2022 Font upload & CA font parity\n\u2022 Brand voice profile\n\u2022 Brand Kit regression suite\n\u2022 Copy/paste formatting normalization\n\u2022 Content Studio stability\n\u2022 Canva sync reliability\n\u2022 Builder SLO contract",
     "\u2022 Light/dark mode & background images\n\u2022 Inline link checker & deliverability\n\u2022 Brand fonts in LP & forms\n\u2022 Brand compliance score\n\u2022 Brand Kit maturity dashboard\n\u2022 Folder mgmt in Content Studio",
     "\u2022 Multi-brand kits per account",
     "\u2022 Real-time co-editing\n\u2022 Block-level comments & @-mentions\n\u2022 Approval workflow & version history\n\u2022 Locked layouts for governance\n\u2022 Cross-account brand inheritance"],
    ["Universal Builder, Portability & Migration",
     "\u2022 Universal Content block primitive\n\u2022 Auto-migration of saved blocks\n\u2022 Bulk migration tool STARTS\n\u2022 Builder Code Mode STARTS",
     "\u2022 Bulk migration tool SHIPS\n\u2022 1:1 migration tool\n\u2022 Builder Code Mode SHIPS\n\u2022 Builder Liquid templating\n\u2022 Brand Kit auto-applied to UC\n\u2022 Template categorization fix",
     "\u2022 UC blocks render in CJB\n\u2022 UC audit & version history",
     "\u2022 Funded migration program"],
    ["AI-Powered Builder & Accelerated Time to Value",
     "\u2022 Brand Kit auto-extract on signup\n\u2022 AI Email Setup Agent STARTS\n\u2022 Write with AI quality improvements",
     "\u2022 Industry-specific templates\n\u2022 AI Email Setup Agent SHIPS\n\u2022 B2B & ProServ gallery\n\u2022 Industry-aware gallery\n\u2022 Ecommerce lifecycle templates\n\u2022 Store-connected preview\n\u2022 AI image gen from catalog\n\u2022 Image Remix\n\u2022 In-canvas revenue per recipient",
     "\u2022 Per-recipient dynamic images\n\u2022 Per-profile Smart Send & A/B\n\u2022 Lifecycle coverage gap analyzer\n\u2022 Goal-driven campaign agent\n\u2022 Conversational email refinement",
     "\u2022 AI brand-style transfer\n\u2022 Campaign brief to multi-variant\n\u2022 Store intelligence in generation"],
    ["Unified Omni-Channel Builder & Activation",
     "\u2022 Brand-Kit-aware generative SMS",
     "\u2022 SMS variant gen & A/B\n\u2022 DRAFT-resurrect campaign",
     "\u2022 Shared blocks in email + SMS\n\u2022 Cross-channel preview\n\u2022 Brand Kit on SMS short links\n\u2022 Contextual discovery prompts",
     "\u2014"]
]

table = doc.add_table(rows=len(roadmap_data), cols=5)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, row_data in enumerate(roadmap_data):
    for j, cell_text in enumerate(row_data):
        cell = table.cell(i, j)
        add_table_cell_text(cell, cell_text, bold=(i == 0 or j == 0), size=8)
        if i == 0:
            set_cell_shading(cell, 'D9E2F3')
        elif j == 0:
            set_cell_shading(cell, 'F2F2F2')

# ============ PAGE BREAK + BUSINESS CASE ============
doc.add_page_break()
doc.add_heading('Business Case & Projections', level=1)
doc.add_paragraph('FY26 baseline \u2192 FY27 targets. Editor-attributed ARR model across paid, free, and trial cohorts using conservative causal shares.')

doc.add_heading('FY26 Baselines', level=2)
baseline_data = [
    ["Metric", "Value", "Metric", "Value"],
    ["Paid Active Users/mo", "1,015,648", "Free Active Users/mo", "870,303"],
    ["Bulk Established/mo", "888,706", "Free Established/mo", "313,806"],
    ["Bulk Adoption Rate", "92.7%", "Free Bulk Adoption", "75.0%"],
    ["Bulk Activation Rate", "60.6%", "Free Bulk Activation", "48.1%"],
    ["30-Day Repeat Send Rate", "83.2%", "Bulk Churn", "40.0% (+2.1pp YoY)"],
    ["Overall CSAT", "3.87/5 (73.2% Good+)", "Trial Activation", "10.8%"],
    ["Median Days to First Send", "5\u20136 days", "ARPU (steady-state)", "$91.44/mo ($1,097/yr)"]
]

table = doc.add_table(rows=len(baseline_data), cols=4)
table.style = 'Table Grid'
for i, row_data in enumerate(baseline_data):
    for j, cell_text in enumerate(row_data):
        cell = table.cell(i, j)
        add_table_cell_text(cell, cell_text, bold=(i == 0), size=9)
        if i == 0:
            set_cell_shading(cell, 'D9E2F3')

doc.add_heading('Leading Indicators: Baselines & Targets', level=2)
li_data = [
    ["Leading Indicator", "FY26 Baseline", "FY27 Target", "Lift"],
    ["Builder Adoption", "92.7% (paid) / 75.0% (free)", "95% / 82%", "+2.3pp / +7.0pp"],
    ["Builder Activation", "60.6% (paid) / 48.1% (free)", "67% / 55%", "+6.4pp / +6.9pp"],
    ["30-Day Repeat Send Rate", "83.2% (paid) / 73.4% (free)", "87% / 80%", "+3.8pp / +6.6pp"],
    ["Overall CSAT", "3.87/5 (73.2% Good+)", "4.2/5 (85% Good+)", "+0.33 avg"],
    ["Ease of Use CSAT", "3.53/5 (54% Easy+)", "4.0/5 (70% Easy+)", "+0.47 avg"],
    ["Site Performance CSAT", "3.86/5 (72.9% Good+)", "4.2/5 (85% Good+)", "+0.34 avg"],
    ["Trial Activation", "10.8%", "16%", "+5.2pp"]
]

table = doc.add_table(rows=len(li_data), cols=4)
table.style = 'Table Grid'
for i, row_data in enumerate(li_data):
    for j, cell_text in enumerate(row_data):
        cell = table.cell(i, j)
        add_table_cell_text(cell, cell_text, bold=(i == 0), size=9)
        if i == 0:
            set_cell_shading(cell, 'D9E2F3')

doc.add_heading('Projected Business Impact', level=2)
pi_data = [
    ["Cohort", "Key Levers", "Editor-Attributed ARR"],
    ["Paid Cohort", "Adoption (+2.3pp), Activation (+6.4pp), 30-day repeat (+3.8pp), CSAT recovery", "$6.7M"],
    ["Free Cohort", "Adoption (+7.0pp), Activation (+6.9pp), 30-day repeat (+6.6pp), CSAT recovery", "$8.7M"],
    ["Trial Cohort", "Trial activation (+5.2pp), 30-day repeat (+7.2pp)", "$5.6M"]
]

table = doc.add_table(rows=len(pi_data), cols=3)
table.style = 'Table Grid'
for i, row_data in enumerate(pi_data):
    for j, cell_text in enumerate(row_data):
        cell = table.cell(i, j)
        add_table_cell_text(cell, cell_text, bold=(i == 0 or j == 2), size=9)
        if i == 0:
            set_cell_shading(cell, 'D9E2F3')

doc.add_paragraph('')
p = doc.add_paragraph()
run = p.add_run('Total Editor-Attributed Annual Revenue Impact: ~$21.0M')
run.bold = True
run.font.size = Pt(14)
p = doc.add_paragraph()
p.add_run('$6.7M from Paid Cohort (32%) | $8.7M from Free Cohort (41%) | $5.6M from Trial Cohort (27%)').font.size = Pt(10)

doc.save('/Users/dprabhakara/Downloads/FY27_Unified_Builder_Strategy_Roadmap.docx')
print('Done! File saved.')
