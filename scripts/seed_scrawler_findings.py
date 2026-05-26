#!/usr/bin/env python3
"""Seed findings JSONL for a partial run (auth blocked) + login UX observations."""

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cjb-scrawler" / "findings" / "run-2026-05-26.jsonl"
RUN_ID = "2026-05-26"
TS = datetime.now(timezone.utc).isoformat()


def row(**kwargs) -> dict:
    base = {
        "run_id": RUN_ID,
        "evidence": {"url": "https://login.mailchimp.com/", "timestamp": TS},
    }
    base.update(kwargs)
    return base


ECOM_STEPS = [
    ("ecom_00_nav", 1, "Navigate to Customer Journey / Create"),
    ("ecom_01_intent", 1, "Choose welcome template or blank journey"),
    ("ecom_02_trigger", 2, "Set tag scrawler-ecom-test or signup trigger"),
    ("ecom_03_email1", 4, "Welcome + brand intro email"),
    ("ecom_04_delay1", 3, "Add 2-day delay"),
    ("ecom_05_email2", 4, "Social proof / bestsellers email"),
    ("ecom_06_delay2", 3, "Add 3-day delay"),
    ("ecom_07_email3", 4, "First-purchase 10% off email"),
    ("ecom_08_review", 6, "Review journey without Turn on"),
    ("ecom_09_save", 6, "Save as Draft"),
]

PROSERV_STEPS = [
    ("proserv_00_nav", 1, "Create journey avoiding ecom-only templates"),
    ("proserv_01_template", 1, "Assess ProServ template catalog skew"),
    ("proserv_02_trigger", 2, "Tag scrawler-proserv-lead trigger"),
    ("proserv_03_email1", 4, "Personal intro email"),
    ("proserv_04_delay1", 3, "3-day delay"),
    ("proserv_05_email2", 4, "Value content email (no cart language)"),
    ("proserv_06_delay2", 3, "2-day delay"),
    ("proserv_07_email3", 4, "Consultation booking CTA"),
    ("proserv_08_branch", 5, "If/else on appointment-booked tag"),
    ("proserv_09_review", 6, "Review Draft only"),
    ("proserv_10_save", 6, "Save Draft"),
]

EXTRA = [
    row(
        persona="setup",
        step_id="setup_login_cookie",
        stage=2,
        status="fail",
        title="Cookie consent panel obscures login on first visit",
        observed="Large OneTrust preference center visible before dismiss; extra click required.",
        expected="Minimal friction to reach login fields.",
        severity="P3",
        known_theme=None,
        novel=True,
        engineering_lane="cjb_canvas_ui",
    ),
    row(
        persona="setup",
        step_id="setup_login_split",
        stage=2,
        status="pass",
        title="Intuit login shows email-first step",
        observed="Only Username/Email field visible initially; Log in button present without password on same screen.",
        expected="Clear progression to password or SSO.",
        severity="—",
    ),
    row(
        persona="setup",
        step_id="setup_login_invalid",
        stage=2,
        status="fail",
        title="Invalid email Log in does not surface password or inline error in snapshot",
        observed="Clicked Log in with test email; remained on same login URL without password field in a11y tree.",
        expected="Password step or validation message.",
        severity="P2",
        novel=True,
        engineering_lane="unknown",
    ),
]

BLOCKED_OBS = (
    "CJB step not executed: MC_EMAIL/MC_PASSWORD missing in cjb-scrawler/.env. "
    "Re-run after adding credentials (see cjb-scrawler/README.md)."
)

DESK_ALIGN = {
    "ecom_01_intent": (
        "Trigger Selection List Not Searchable",
        "Flow Templates Have No Search / Filter",
        "Better Templates / Pre-built Flows",
    ),
    "ecom_02_trigger": ("Trigger Selection List Not Searchable",),
    "ecom_03_email1": ("Brand Kit Not Applied to Automation Email Templates", "CJB Still Uses Legacy Editor"),
    "ecom_04_delay1": ("Slow / Confusing Journey Builder UX",),
    "ecom_08_review": ("Premature 'Turn On' / Activation Before Content Ready",),
    "proserv_01_template": ("Better Templates / Pre-built Flows",),
    "proserv_08_branch": ("Advanced Segmentation in CJB",),
}


def main() -> None:
    lines = []
    if OUT.is_file():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if line.strip():
                lines.append(json.loads(line))
    existing_ids = {r.get("step_id") for r in lines}

    for r in EXTRA:
        if r["step_id"] not in existing_ids:
            lines.append(r)

    for persona, steps in (("ecom", ECOM_STEPS), ("proserv", PROSERV_STEPS)):
        for step_id, stage, title in steps:
            if step_id in existing_ids:
                continue
            themes = DESK_ALIGN.get(step_id, ())
            lines.append(
                row(
                    persona=persona,
                    step_id=step_id,
                    stage=stage,
                    status="blocked",
                    title=title,
                    observed=BLOCKED_OBS
                    + (
                        f" Desk-research themes to validate: {', '.join(themes)}."
                        if themes
                        else ""
                    ),
                    expected=f"Per cjb-scrawler/personas/{'ecommerce' if persona == 'ecom' else 'proserv'}.md",
                    severity="P0" if step_id.endswith("_save") else "P1",
                    known_theme=themes[0] if themes else None,
                    novel=not themes,
                    engineering_lane="cjb_canvas_ui",
                    roadmap_link="mailchimp.html BET 3" if persona == "proserv" and "template" in step_id else None,
                )
            )

    OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in lines) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(lines)} rows to {OUT}")


if __name__ == "__main__":
    main()
