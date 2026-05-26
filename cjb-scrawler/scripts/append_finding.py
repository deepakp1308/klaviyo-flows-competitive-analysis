#!/usr/bin/env python3
"""Append one JSON finding line to cjb-scrawler/findings/<run_id>.jsonl."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FINDINGS_DIR = Path(__file__).resolve().parent.parent / "findings"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: append_finding.py '<json object>' OR read JSON from stdin", file=sys.stderr)
        sys.exit(1)
    raw = sys.argv[1] if sys.argv[1] != "-" else sys.stdin.read()
    row = json.loads(raw)
    run_id = row.get("run_id") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row.setdefault("evidence", {})
    row["evidence"].setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    FINDINGS_DIR.mkdir(parents=True, exist_ok=True)
    path = FINDINGS_DIR / f"run-{run_id}.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(path)


if __name__ == "__main__":
    main()
