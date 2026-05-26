# CJB Scrawler

Live UX audit for Mailchimp Customer Journey Builder. See `.cursor/skills/cjb-scrawler/SKILL.md`.

## Quick start

1. Copy `cjb-scrawler/.env.example` → `cjb-scrawler/.env` and set `MC_EMAIL` / `MC_PASSWORD`.
2. In Cursor, ask: **Run CJB Scrawler** (loads the skill + browser MCP).
3. Complete 2FA in the browser when prompted.
4. Regenerate report:

```bash
python3 scripts/build_cjb_scrawler_report.py
```

## Artifacts

| Path | Purpose |
|------|---------|
| `findings/run-*.jsonl` | Raw step logs (gitignored) |
| `fix-backlog.md` | Prioritized fix cards |
| `../cjb-scrawler-report.html` | GitHub Pages report (deduped issues + step logs) |
| `../cjb-marketer-audit/` | **Standalone** screenshot-by-screenshot marketer audit — [live URL](https://deepakp1308.github.io/klaviyo-flows-competitive-analysis/cjb-marketer-audit/) |
| `screenshots/run-<date>/{step_id}.png` | Per-frame captures (gitignored); paths referenced in walkthrough |

## Log a finding manually

```bash
python3 cjb-scrawler/scripts/append_finding.py '{"run_id":"2026-05-26","persona":"ecom","step_id":"ecom_02_trigger","stage":2,"status":"fail","title":"...","observed":"...","expected":"...","severity":"P1","evidence":{"url":"https://..."}}'
```
