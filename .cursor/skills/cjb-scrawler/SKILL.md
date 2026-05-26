---
name: cjb-scrawler
description: >-
  Build Mailchimp CJB automation flows as e-commerce and ProServ personas via
  browser automation; log usability issues, bugs, and barriers against the
  8-stage CJB workflow taxonomy; output JSONL findings and HTML report. Use when
  the user says CJB Scrawler, run scrawler, live CJB UX audit, or persona flow
  build on Mailchimp Customer Journey Builder.
---

# CJB Scrawler

Live UX audit agent for Mailchimp **Customer Journey Builder (CJB)**. Builds two Draft journeys on a real account, captures friction, and synthesizes fix proposals mapped to repo evidence (`mailchimp.html`, `cjb-workflow-health.html`).

## Non-negotiables

1. **Draft only** — never click **Turn on** / activate. If prompted, cancel and log a finding (stage 6–7).
2. **Test audience only** — list `Scrawler QA`, tags `scrawler-ecom-test` / `scrawler-proserv-lead`; no production segments.
3. **Naming** — prefix `Scrawler_` on journeys, lists, tags.
4. **Credentials** — `MC_EMAIL` / `MC_PASSWORD` from env only; never commit, never paste into HTML/JSONL/report.
5. **2FA** — pause and ask the user to complete in the browser; resume with `browser_snapshot`.
6. **Stop** — login fails twice; same step deadlocks three times; unexpected "flow is live" banner.

## Pre-flight

1. Read [cjb-scrawler/personas/ecommerce.md](cjb-scrawler/personas/ecommerce.md) and [proserv.md](cjb-scrawler/personas/proserv.md).
2. Read stage taxonomy in [generate_cjb_workflow_health.py](generate_cjb_workflow_health.py) (`STAGE_META`).
3. Confirm env: `MC_EMAIL`, `MC_PASSWORD` (optional `MC_ACCOUNT_LABEL` for report).
4. Open browser → `https://login.mailchimp.com/` → login.
5. Create if missing: audience/list **Scrawler QA** (&lt;5 test contacts), tags above.
6. Initialize run log: `cjb-scrawler/findings/run-<ISO-date>.jsonl`.

## Browser workflow (cursor-ide-browser)

- `browser_navigate` → login → Automations / Customer Journeys.
- `browser_lock` before multi-step canvas work; `unlock` when done.
- After each playbook step: append one JSONL line (schema in [findings-schema.json](cjb-scrawler/findings-schema.json)).
- P0/P1: `browser_take_screenshot` → `cjb-scrawler/screenshots/` (gitignored).
- P2/P3: snapshot only unless user asks for screenshots.

## Persona runs (order)

### A — E-commerce: `Scrawler_Ecom_Welcome_FirstPurchase`

Playbook: [ecommerce.md](cjb-scrawler/personas/ecommerce.md). Target: welcome + 2 delays + 3 emails; tag/signup trigger.

### B — ProServ: `Scrawler_ProServ_LeadNurture_Appointment`

Playbook: [proserv.md](cjb-scrawler/personas/proserv.md). Avoid abandoned-cart templates; nurture + consultation CTA; optional if/else on `appointment-booked`.

## Finding record (append JSONL)

Each line validates against `findings-schema.json`. Required fields:

- `run_id`, `persona` (`ecom`|`proserv`), `step_id`, `stage` (1–8), `status` (`pass`|`fail`|`blocked`)
- `title`, `observed`, `expected`, `severity` (`P0`–`P3`)
- `evidence`: `{ "url", "timestamp" }` (+ `screenshot` if captured)
- Optional: `known_theme`, `novel`, `hvc_mrr_proxy`, `engineering_lane`, `roadmap_link`

**Severity**

| Level | When |
|-------|------|
| P0 | Data loss, live send risk, auth broken, journey won't save |
| P1 | Cannot complete majority flow without workaround |
| P2 | Confusing/slow; workaround exists |
| P3 | Polish / copy / minor UI |

## Post-run synthesis

1. Dedupe by normalized `title` + `stage` → `symptom_hash`.
2. Map to HVC themes in `mailchimp.html` → set `known_theme` or `novel: true`.
3. Write fix cards to [cjb-scrawler/fix-backlog.md](cjb-scrawler/fix-backlog.md) (10-field format in plan).
4. Run: `python3 scripts/build_cjb_scrawler_report.py` and `python3 scripts/synthesize_scrawler_fix_backlog.py`
5. Optional Playwright runner (same playbooks): `python3 scripts/run_cjb_scrawler_playwright.py`
6. End-of-persona QC: Draft saved, ≥3 emails, ≥2 delays, status ≠ Live.

## Watch-for (probe actively)

- Trigger modal not searchable (stage 2)
- Ecom-skewed template gallery for ProServ (stage 1)
- Premature Turn On affordance (stage 6–7)
- 1-hour minimum delay (stage 3)
- Re-entry defaults reset after save (stage 7)
- Legacy editor vs NEB on email steps (stage 4)
- Template link opens help article (stage 1)
- Canvas scroll / replication glitches (stage 3–4)

## Outputs

| Artifact | Path |
|----------|------|
| Raw log | `cjb-scrawler/findings/*.jsonl` |
| Fix backlog | `cjb-scrawler/fix-backlog.md` |
| HTML report | `cjb-scrawler-report.html` |

Do not commit `.env`, JSONL, or screenshots.
