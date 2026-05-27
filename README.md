# Klaviyo Flows Competitive Analysis

**Live site:** [deepakp1308.github.io/klaviyo-flows-competitive-analysis](https://deepakp1308.github.io/klaviyo-flows-competitive-analysis/)

An AI-agent-powered competitive intelligence platform that produces multi-layered strategy briefs for Mailchimp's automation and editor products. Covers Klaviyo, Shopify, six emerging threats, and Mailchimp's own Unified Builder and CJB roadmap — synthesized from 28K+ Voice-of-Customer data points, BigQuery product health telemetry, internal repo forensics, and live browser-based UX audits.

---

## Purpose

This repo serves as the **central competitive analysis knowledge base** for Mailchimp's Marketing Automation (CJB) and Unified Builder (Editor) product lines. It exists to:

1. **Inform FY27 strategy** — Surfaces 72 initiative gaps across three incumbents and six startups, with competitive-gap-to-roadmap mappings driving a $20–25M automation ARR target.
2. **Ground decisions in evidence** — Every claim traces back through a layered evidence stack (desk research → public VoC → internal Slack HVC → UX research → BigQuery → repo forensics).
3. **Enable live UX auditing** — An AI agent ("CJB Scrawler") autonomously builds Mailchimp automation flows, logs usability findings, and produces prioritized fix backlogs.
4. **Share intelligence** — Static GitHub Pages site makes briefs accessible to product, engineering, design, and leadership without tooling dependencies.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Data Collection Layer                  │
├──────────────┬──────────────┬─────────────┬──────────────┤
│  Competitive │  Public VoC  │ Internal    │  BigQuery    │
│  Desk        │  G2/Reddit/  │ Slack HVC   │  Product     │
│  Research    │  Capterra    │ $299+/mo    │  Health      │
├──────────────┼──────────────┼─────────────┼──────────────┤
│  HeyMarvin   │  Repo        │  PRD Audit  │  CJB Scrawler│
│  50 Videos → │  Forensics   │  9 PDFs     │  Browser UX  │
│  21 Briefs   │  CJB + NUNI  │             │  Automation  │
└──────┬───────┴──────┬───────┴──────┬──────┴──────┬───────┘
       │              │              │             │
       ▼              ▼              ▼             ▼
┌──────────────────────────────────────────────────────────┐
│               Synthesis & Analysis Layer                  │
│                                                          │
│  Qualitative thematic coding → Love/Hate/Mixed buckets   │
│  Net-sentiment scoring (qualitative, not NLP-computed)    │
│  Cross-competitor gap mapping (Klaviyo 26, Shopify 16)    │
│  Initiative Canvas (72 initiatives, P1–P5 priority)      │
│  Strategy 6-Pager, Growth Model, Loss Attribution        │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│                    Output Layer                           │
│                                                          │
│  32 HTML briefs ──→ GitHub Pages (static, no build step) │
│  DOCX exports  ──→ create_all_docs.py / create_docx.py  │
│  Scrawler JSONL ─→ cjb-scrawler/findings/*.jsonl        │
│  Scrawler HTML  ─→ cjb-scrawler-report.html             │
└──────────────────────────────────────────────────────────┘
```

### Cursor AI Agent Integration

This repo is designed to be operated by Cursor AI agents with the following context layers:

| Layer | File | Purpose |
|-------|------|---------|
| **Workspace Rule** | `.cursor/rules/competitive-analysis-knowledge-base.mdc` | Always-on context: document map, derivation methodology, strategic numbers, cross-competitor gaps |
| **Workspace Rule** | `.cursor/rules/cjb-scrawler.mdc` | Guardrails for live CJB UX audits (draft-only, no production data) |
| **Skill** | `.cursor/skills/cjb-scrawler/SKILL.md` | Full playbook for the CJB Scrawler agent: personas, browser workflow, finding schema, synthesis steps |
| **User Rule** | `analytics-ai-primitives.mdc` | Analytics AI roadmap context (R&A team P0 functions, diffusion, Data Guardian) |

The rules ensure agents always know the repo structure, derivation standards, and safety constraints before making any changes.

---

## Document Map

### Core Competitor Briefs

Each brief uses a multi-tab hash-routed structure (`#brief`, `#sentiment`, `#canvas`, etc.):

| File | Subject | VoC Sample |
|------|---------|------------|
| `index.html` | **Klaviyo Flows** — Flows AI, Marketing Agent, predictive triggers, 5-channel canvas | 600+ reviews/threads |
| `mailchimp.html` | **Mailchimp CJB** — 13-tab FY27 strategy dossier (Initiative Canvas, Growth Model, Loss Attribution) | 14K+ public + Slack HVC + HeyMarvin |
| `shopify.html` | **Shopify Marketing Automations + Flow** — Sidekick/Magic, native commerce data | 10K+ reviews/threads |
| `emerging-threats.html` | **6 Startups** — Customer.io, Attentive, Auxia, Postscript, Mailmodo, Loops | 3K+ reviews/threads |

### Mailchimp Internal Strategy

| File | Subject |
|------|---------|
| `mailchimp-editor.html` | 18-tab unified editor/builder brief (NEB, SMS, Brand Kit, Freddie) |
| `unified-builder-roadmap.html` | FY27 Unified Builder roadmap |
| `unified-builder-vp-swimlanes.html` | VP-level swimlane view |
| `unified-builder-critical-path.html` | Critical path dependencies |
| `unified-builder-revenue-attribution.html` | Revenue attribution model (~$21M ARR) |
| `unified-builder-workflow-health.html` | Workflow health metrics |
| `unified-builder-competitive-position.html` | Competitive position assessment |

### Repo Forensics & Freddie Analysis

| File | Subject |
|------|---------|
| `cjb-repo-analysis.html` | CJB backend forensic — 13 repos, C2 re-platform, UI in monolith |
| `nuni-repo-analysis.html` | NUNI editor forensic — 62 repos, schema drift, AI UI 8x faster |
| `freddie-concerns.html` | 3 structural concerns: foundation pain, Canva/Klaviyo gap, NEA stalled |
| `freddie-deepak-phase1.html` | Canva-gap creative parity analysis |
| `freddie-deepak-phase2.html` | Mailchimp-native send-time capabilities |

### CJB Scrawler Live Audits

| File | Subject |
|------|---------|
| `cjb-scrawler-report.html` | AI-generated CJB UX audit report |
| `cjb-scrawler-marketer-walkthrough.html` | Marketer persona walkthrough |
| `cjb-workflow-audit/` | Workflow audit with screenshots |
| `cjb-marketer-audit/` | Marketer persona audit with SVG figures |
| `cjb-kateco-audit/` | Kate Co brand audit |
| `cjb-realflow-audit/` | Real-flow replication audit |

### Editor & Standard Builder Audits

| File | Subject |
|------|---------|
| `std-editor-deep-audit.html` | Standard editor deep audit |
| `std-editor-scrawler-report.html` | Standard editor scrawler findings |
| `ub-scrawler-report.html` | Unified builder scrawler findings |
| `editor/index.html` | Editor analysis |
| `conversational-email-editor.html` | Conversational email editor concept |

### TestJam (AI Builder Evaluation)

| File | Subject |
|------|---------|
| `testjam-execution-report.html` | Kate Co 105-block replication + 25 use cases |
| `testjam-ai-builder-usecases.html` | AI Unified Builder evaluation use cases |

### Prototypes

| Directory | Subject |
|-----------|---------|
| `freddie-deepak-phase1-prototype/` | Interactive prototype: Canva-gap creative parity (HTML/JS/CSS) |
| `freddie-deepak-phase2-prototype/` | Interactive prototype: send-time capabilities (HTML/JS/CSS) |

---

## Derivation Methodology

All analysis follows a layered evidence stack — each layer adds rigor:

1. **Competitive desk research** — Product pages, help centers, pricing, case studies; third-party comparisons (Costbench, Jellyreach, Omnisend, etc.)
2. **Public VoC** — Qualitative thematic synthesis from G2, Trustpilot, Capterra, Reddit, vendor communities, agency blogs, YouTube. Coded into Love/Hate/Mixed + net-sentiment scores (qualitative, not NLP-computed).
3. **Slack HVC VoC** — `#hvc_feedback`, `#mc-hvc-escalations`, `#mc-feedback-summary`; HVC = $299+/mo MRR customers; deduplicated by user + quote
4. **HeyMarvin UX research** — 50 videos → Whisper transcription → 21 customer briefs → synthesis
5. **BigQuery product health** — `bi_aggregate.product_journey_monthly` (89.4M rows); stages: Unexplored → Explore → Try → Establish → Abandon
6. **PRD audit** — 9 PDFs mapped to evidence gaps
7. **Repo forensics** — CJB (`crmmktg-mktauto`) and NUNI (`collab-email`) GitHub org analysis
8. **CJB Scrawler** — Live browser automation building real Mailchimp flows, logging usability findings against 8-stage workflow taxonomy
9. **Cross-tab synthesis** — Initiative Canvas (72 initiatives), Strategy 6-Pager, Growth Model, Loss Attribution

---

## Key Strategic Numbers

| Metric | Value |
|--------|-------|
| FY27 automation ARR target | +$20–25M (lower band of $20–32M envelope) |
| HVC MRR exposure (automation) | $177.5K/mo across 73 themes |
| HVC MRR exposure (nav/search) | $70K/mo (separate) |
| CJB Established users | 132K (+18.4% YoY) |
| CJB Activation rate | 33.6% |
| CJB Churn rate | 40.2% |
| Free CJB adoption | 1.1% |
| Binding constraint | Activation funnel (customers use 10–20% of features) |
| Critical dependency | Eventbus migration gates P3–P5 |

---

## Tools & Technologies

| Tool | Role |
|------|------|
| **Cursor IDE + AI Agents** | Primary authoring and analysis environment; agents use rules/skills for context |
| **GitHub Pages** | Static hosting — no build step, pure HTML/CSS/JS |
| **Chart.js** | Interactive charts embedded in HTML briefs |
| **Python** | Doc generators (`create_all_docs.py`, `create_docx.py`, `generate_roadmap_docx.py`), CJB workflow health generation, scrawler scripts |
| **Slack MCP** | Pulls HVC feedback from internal Slack channels |
| **BigQuery MCP** | Queries product health telemetry |
| **Browser Automation** | CJB Scrawler uses `cursor-ide-browser` for live Mailchimp UX audits |
| **HeyMarvin** | UX research video transcription and synthesis |

---

## How to Use This Output

### For Product Strategy
- Start with `mailchimp.html` **Initiative Canvas** tab — see all 72 initiatives mapped to competitive gaps
- Cross-reference with `index.html` (Klaviyo), `shopify.html`, `emerging-threats.html` for competitor-specific depth
- Use the **Growth Model** and **Loss Attribution** tabs to connect gaps to revenue impact

### For Engineering Planning
- `cjb-repo-analysis.html` and `nuni-repo-analysis.html` show technical debt and migration state
- `unified-builder-critical-path.html` shows dependency chains gating delivery
- CJB Scrawler reports surface bugs/friction with severity and engineering lane annotations

### For Design
- CJB audit reports (`cjb-workflow-audit/`, `cjb-marketer-audit/`, etc.) include screenshots and persona-specific friction logs
- `freddie-deepak-phase1-prototype/` and `phase2-prototype/` are interactive HTML prototypes

### For Leadership
- `unified-builder-roadmap.html` + `unified-builder-vp-swimlanes.html` give roadmap-level views
- `unified-builder-revenue-attribution.html` connects initiatives to ARR

---

## Running Locally

No build step required — open any `.html` file in a browser.

### Generate DOCX Exports

```bash
python create_all_docs.py      # exports all unified builder content
python create_docx.py           # single-doc export
python generate_roadmap_docx.py # roadmap-specific export
```

### Run CJB Scrawler (Cursor Agent)

The CJB Scrawler is a Cursor AI agent skill, not a standalone script. To run it:

1. Open this repo in Cursor IDE
2. Set environment variables: `MC_EMAIL`, `MC_PASSWORD`
3. Tell the agent: "Run CJB Scrawler" — it reads `.cursor/skills/cjb-scrawler/SKILL.md` and executes the full persona-based UX audit

### Generate CJB Workflow Health

```bash
python generate_cjb_workflow_health.py
```

---

## Repository Structure

```
├── index.html                         # Klaviyo Flows competitive brief
├── mailchimp.html                     # Mailchimp CJB 13-tab strategy dossier
├── shopify.html                       # Shopify automations brief
├── emerging-threats.html              # 6 startup threat briefs
├── mailchimp-editor.html              # 18-tab unified editor brief
├── unified-builder-*.html (6)         # FY27 Unified Builder strategy docs
├── cjb-repo-analysis.html            # CJB backend forensic
├── nuni-repo-analysis.html           # NUNI editor forensic
├── freddie-concerns.html             # Freddie structural concerns
├── freddie-deepak-phase1.html        # Canva-gap analysis
├── freddie-deepak-phase2.html        # Send-time capabilities
├── cjb-workflow-health.html          # CJB workflow health metrics
├── cjb-scrawler-report.html          # AI-generated UX audit report
├── cjb-scrawler-marketer-walkthrough.html
├── std-editor-*.html                  # Standard editor audit reports
├── ub-scrawler-report.html           # Unified builder scrawler report
├── conversational-email-editor.html  # Conversational editor concept
├── testjam-*.html                    # AI builder evaluation reports
├── cjb-workflow-audit/               # Workflow audit + screenshots
├── cjb-marketer-audit/               # Marketer persona audit + SVGs
├── cjb-kateco-audit/                 # Kate Co audit + screenshots
├── cjb-realflow-audit/               # Real-flow replication audit
├── editor/                           # Editor analysis
├── freddie-deepak-phase1-prototype/  # Interactive HTML/JS prototype
├── freddie-deepak-phase2-prototype/  # Interactive HTML/JS prototype
├── cjb-scrawler/                     # Scrawler agent: schemas, personas, scripts
├── scripts/                          # Build scripts for audits and tabs
├── create_all_docs.py                # DOCX export: all unified builder content
├── create_docx.py                    # DOCX export: single document
├── generate_roadmap_docx.py          # DOCX export: roadmap
├── generate_cjb_workflow_health.py   # CJB workflow health generator
└── .cursor/                          # Cursor AI agent context
    ├── rules/                        #   Always-on workspace rules
    └── skills/                       #   Agent skills (CJB Scrawler)
```

---

## Contributing

- Preserve cross-links between briefs (toolbar nav pattern)
- Maintain multi-tab hash routing (`#brief`, `#sentiment`, `#canvas`, etc.)
- VoC claims must cite derivation method and sample size
- Mailchimp internal tabs reference Intuit-internal sources — handle accordingly
- Competitor briefs frame insights from the Mailchimp "what it means for us" perspective

---

## Author

**Deep Prabhakara** — Product Manager, Mailchimp Reporting & Analytics / Marketing Automation
