#!/usr/bin/env python3
"""Generate cjb-scrawler/fix-backlog.md from findings JSONL."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINDINGS_DIR = ROOT / "cjb-scrawler" / "findings"
OUT = ROOT / "cjb-scrawler" / "fix-backlog.md"

HVC_MRR = {
    "Trigger Selection List Not Searchable": "~$16K/mo cluster",
    "Premature 'Turn On' / Activation Before Content Ready": "~$11,384/mo",
    "Editor / UI Glitches in Journey Builder": "~$10,559/mo",
    "Event-Property Access in Flow Branches/Emails": "~$10,000/mo",
    "Flow Templates Have No Search / Filter": "~$10,000/mo",
    "Better Templates / Pre-built Flows": "BET 3 / UR ProServ gap",
    "Advanced Segmentation in CJB": "~$3,000/mo",
    "Brand Kit Not Applied to Automation Email Templates": "HVC theme",
    "CJB Still Uses Legacy Editor": "HVC + NEB migration",
    "Slow / Confusing Journey Builder UX": "~$5,205/mo",
    "Pop-ups / Forms Not Feeding Flows": "UR Watch Party",
    "No Frequency Cap / Suppression Across Flows": "~$2,576/mo",
}


def load_rows() -> list[dict]:
    rows = []
    for path in sorted(FINDINGS_DIR.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def card(r: dict, n: int) -> str:
    fix = r.get("fix_proposal") or {}
    theme = r.get("known_theme") or ""
    mrr = r.get("hvc_mrr_proxy") or HVC_MRR.get(theme, "—")
    repro = fix.get("repro_steps") or [
        f"Persona: {r.get('persona')}",
        f"Step: {r.get('step_id')}",
        f"Observed: {r.get('observed', '')[:200]}",
    ]
    return f"""### {n}. [{r.get('severity', '—')}] {r.get('title', 'Issue')}

1. **Problem:** {fix.get('problem') or r.get('title')}
2. **Repro:** {'; '.join(repro) if isinstance(repro, list) else repro}
3. **Stage / persona:** {r.get('stage')} / {r.get('persona')}
4. **Severity / MRR proxy:** {r.get('severity')} / {mrr}
5. **Root-cause hypothesis:** {fix.get('root_cause_hypothesis') or ('UX' if r.get('status') == 'fail' else 'Blocked run — capability unverified live')}
6. **Proposed fix:** {fix.get('proposed_fix') or _default_fix(r)}
7. **Engineering lane:** {r.get('engineering_lane', 'cjb_canvas_ui')}
8. **Roadmap link:** {r.get('roadmap_link') or _roadmap(theme)}
9. **Validation:** Re-run Scrawler step `{r.get('step_id')}` after fix; confirm Draft journey completes.
10. **Effort / confidence:** {fix.get('effort', 'M')} / {fix.get('confidence', 'M')}

"""


def _default_fix(r: dict) -> str:
    theme = r.get("known_theme")
    if theme == "Trigger Selection List Not Searchable":
        return "Add search/filter to Starting Points modal; surface signup/tag triggers first for SMB."
    if theme == "Better Templates / Pre-built Flows":
        return "Ship B2B/ProServ template category (BET 3): nurture, appointment reminder, post-consult follow-up."
    if theme == "Premature 'Turn On' / Activation Before Content Ready":
        return "Gate Turn on until required steps configured; confirm modal with test send."
    if theme == "Advanced Segmentation in CJB":
        return "Enable tag-based if/else without pre-audience segmentation for simple ProServ branches."
    if r.get("step_id") == "setup_00_credentials":
        return "Operator configures cjb-scrawler/.env; document app-password + 2FA handoff in README."
    if r.get("novel"):
        return "Investigate live repro on next authenticated Scrawler run."
    return "Validate on next live Scrawler pass; align with mailchimp.html Initiative Canvas."


def _roadmap(theme: str | None) -> str:
    if not theme:
        return "mailchimp.html — Initiative Canvas / HVC Risk Map"
    if "Template" in theme or "Pre-built" in theme:
        return "mailchimp.html BET 3 · B2B/ProServ templates; cjb-repo-analysis prebuilt-journey-service archived"
    if "Trigger" in theme:
        return "cjb-workflow-health.html Stage 2 · searchable triggers initiative"
    if "Turn On" in theme:
        return "cjb-workflow-health.html Stage 6–7 · activation guardrails"
    return "mailchimp.html HVC Risk Map"


def main() -> None:
    rows = load_rows()
    issues = [r for r in rows if r.get("status") in ("fail", "blocked")]
    # Dedupe by title+stage
    seen = set()
    unique = []
    for r in sorted(issues, key=lambda x: ({"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(x.get("severity", "P3"), 9))):
        key = (r.get("stage"), r.get("title", "")[:80])
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)

    parts = [
        "# CJB Scrawler — Fix backlog\n",
        f"_Generated from {len(rows)} step logs, {len(unique)} deduped issues._\n",
        "## Run summary\n",
        "- **Auth:** Partial — credentials not in `cjb-scrawler/.env`; CJB canvas steps blocked.\n",
        "- **Login UX:** Cookie banner + Intuit email-first login observed via browser MCP.\n",
        "- **Next:** Add `.env`, re-run `python3 scripts/run_cjb_scrawler_playwright.py` or Cursor skill.\n",
        "\n## Prioritized fix cards\n",
    ]
    for i, r in enumerate(unique, 1):
        parts.append(card(r, i))

    parts.append("\n## Persona journey targets (Draft)\n")
    parts.append("| Persona | Journey | Status |\n|---------|---------|--------|\n")
    parts.append("| E-commerce | `Scrawler_Ecom_Welcome_FirstPurchase` | Blocked at auth |\n")
    parts.append("| ProServ | `Scrawler_ProServ_LeadNurture_Appointment` | Blocked at auth |\n")

    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({len(unique)} cards)")


if __name__ == "__main__":
    main()
