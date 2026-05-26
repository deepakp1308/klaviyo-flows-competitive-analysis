#!/usr/bin/env python3
"""Quick log helper used during live runs."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FINDINGS = Path(__file__).resolve().parent.parent / "findings"
RUN_ID = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def log(**kwargs):
    kwargs.setdefault("run_id", RUN_ID)
    kwargs.setdefault("evidence", {})
    kwargs["evidence"].setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    FINDINGS.mkdir(parents=True, exist_ok=True)
    p = FINDINGS / f"run-{RUN_ID}.jsonl"
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(kwargs, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    log(**json.loads(sys.argv[1]))
