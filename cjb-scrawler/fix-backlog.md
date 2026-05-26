# CJB Scrawler — Fix backlog
_Generated from 17 step logs, 4 deduped issues._
## Run summary
- **Auth:** Partial — credentials not in `cjb-scrawler/.env`; CJB canvas steps blocked.
- **Login UX:** Cookie banner + Intuit email-first login observed via browser MCP.
- **Next:** Add `.env`, re-run `python3 scripts/run_cjb_scrawler_playwright.py` or Cursor skill.

## Prioritized fix cards
### 1. [P1] No trigger search

1. **Problem:** No trigger search
2. **Repro:** Persona: ecom; Step: ecom_01_intent; Observed: Category tabs only
3. **Stage / persona:** 1 / ecom
4. **Severity / MRR proxy:** P1 / ~$16K/mo cluster
5. **Root-cause hypothesis:** UX
6. **Proposed fix:** Add search/filter to Starting Points modal; surface signup/tag triggers first for SMB.
7. **Engineering lane:** cjb_canvas_ui
8. **Roadmap link:** cjb-workflow-health.html Stage 2 · searchable triggers initiative
9. **Validation:** Re-run Scrawler step `ecom_01_intent` after fix; confirm Draft journey completes.
10. **Effort / confidence:** M / M

### 2. [P2] Legacy vs New Builder

1. **Problem:** Legacy vs New Builder
2. **Repro:** Persona: ecom; Step: ecom_03_email1; Observed: Automation email opens campaign wizard
3. **Stage / persona:** 4 / ecom
4. **Severity / MRR proxy:** P2 / HVC + NEB migration
5. **Root-cause hypothesis:** UX
6. **Proposed fix:** Validate on next live Scrawler pass; align with mailchimp.html Initiative Canvas.
7. **Engineering lane:** cjb_canvas_ui
8. **Roadmap link:** mailchimp.html HVC Risk Map
9. **Validation:** Re-run Scrawler step `ecom_03_email1` after fix; confirm Draft journey completes.
10. **Effort / confidence:** M / M

### 3. [P2] Emails 3-4 not built

1. **Problem:** Emails 3-4 not built
2. **Repro:** Persona: ecom; Step: ecom_06_delay2; Observed: Partial journey for audit
3. **Stage / persona:** 3 / ecom
4. **Severity / MRR proxy:** P2 / —
5. **Root-cause hypothesis:** Blocked run — capability unverified live
6. **Proposed fix:** Investigate live repro on next authenticated Scrawler run.
7. **Engineering lane:** cjb_canvas_ui
8. **Roadmap link:** mailchimp.html — Initiative Canvas / HVC Risk Map
9. **Validation:** Re-run Scrawler step `ecom_06_delay2` after fix; confirm Draft journey completes.
10. **Effort / confidence:** M / M

### 4. [—] Scrawler QA segment not created

1. **Problem:** Scrawler QA segment not created
2. **Repro:** Persona: setup; Step: setup_04_segment; Observed: Time budget; contacts searchable individually
3. **Stage / persona:** 2 / setup
4. **Severity / MRR proxy:** — / —
5. **Root-cause hypothesis:** Blocked run — capability unverified live
6. **Proposed fix:** Investigate live repro on next authenticated Scrawler run.
7. **Engineering lane:** cjb_canvas_ui
8. **Roadmap link:** mailchimp.html — Initiative Canvas / HVC Risk Map
9. **Validation:** Re-run Scrawler step `setup_04_segment` after fix; confirm Draft journey completes.
10. **Effort / confidence:** M / M


## Persona journey targets (Draft)
| Persona | Journey | Status |
|---------|---------|--------|
| E-commerce | `Scrawler_Ecom_Welcome_FirstPurchase` | Blocked at auth |
| ProServ | `Scrawler_ProServ_LeadNurture_Appointment` | Blocked at auth |
