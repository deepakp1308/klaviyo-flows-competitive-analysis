#!/usr/bin/env python3
"""Generate committed SVG figures for cjb-marketer-audit (GitHub Pages–safe)."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "cjb-marketer-audit" / "index.html"
OUT = ROOT / "cjb-marketer-audit" / "images"

W, H = 960, 540


def svg_frame(step_id: str, title: str, planned: bool = False) -> str:
    badge = "PLANNED — not captured live" if planned else "Live audit · Goodnight Fox · 2026-05-26"
    badge_fill = "#92400e" if planned else "#1e40af"
    lines = [ln.strip() for ln in re.split(r"<br\s*/?>", title, flags=re.I) if ln.strip()]
    if not lines:
        lines = [title]
    body_y = 120
    body_lines = ""
    for i, line in enumerate(lines[:4]):
        body_lines += (
            f'<text x="48" y="{body_y + i * 28}" font-family="Arial,sans-serif" '
            f'font-size="18" fill="#111827">{html.escape(line)}</text>\n'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">{html.escape(step_id)} — {html.escape(lines[0])}</title>
  <rect width="{W}" height="{H}" fill="#f3f4f6"/>
  <rect width="{W}" height="56" fill="#241c15"/>
  <text x="24" y="36" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#ffe01b">Mailchimp</text>
  <text x="200" y="36" font-family="Arial,sans-serif" font-size="14" fill="#e5e7eb">Customer Journey Builder · Goodnight Fox (us17)</text>
  <rect x="24" y="72" width="912" height="380" rx="8" fill="#fff" stroke="#d1d5db" stroke-width="2"/>
  {body_lines}
  <rect x="24" y="468" width="200" height="28" rx="4" fill="{badge_fill}"/>
  <text x="36" y="487" font-family="ui-monospace,monospace" font-size="11" fill="#fff">{html.escape(step_id)}</text>
  <text x="240" y="487" font-family="Arial,sans-serif" font-size="12" fill="#6b7280">{html.escape(badge)}</text>
  <text x="24" y="520" font-family="Arial,sans-serif" font-size="11" fill="#9ca3af">Annotated figure for audit documentation · Replace with PNG when captured</text>
</svg>
"""


def patch_html(content: str, figures: dict[str, str]) -> str:
    pattern = re.compile(
        r'(<div class="frame" id="(?P<id>[^"]+)">.*?'
        r')<div class="shot">(?P<body>.*?)</div>',
        re.DOTALL,
    )

    def repl(m: re.Match) -> str:
        step_id = m.group("id")
        body = m.group("body")
        text = re.sub(r"<[^>]+>", " ", body)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        alt = html.escape(text[:200], quote=True)
        planned = "(Planned)" in text or "not captured" in text.lower()
        fig = figures[step_id]
        cap = f'<figcaption>{body}</figcaption>' if "<br" in body else ""
        return (
            f'{m.group(1)}<figure class="shot">'
            f'<img src="images/{fig}" alt="{alt}" width="100%" height="auto" loading="lazy" decoding="async"/>'
            f"{cap}</figure>"
        )

    return pattern.sub(repl, content)


def main() -> None:
    content = HTML.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    figures: dict[str, str] = {}

    for m in re.finditer(
        r'<div class="frame" id="([^"]+)">.*?<div class="shot">(.*?)</div>',
        content,
        re.DOTALL,
    ):
        step_id = m.group(1)
        body = m.group(2)
        text = re.sub(r"<[^>]+>", " ", body)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        if text.lower().startswith("screenshot:"):
            text = text[11:].strip()
        planned = "(planned)" in text.lower()
        name = f"{step_id}.svg"
        (OUT / name).write_text(svg_frame(step_id, text, planned), encoding="utf-8")
        figures[step_id] = name

    patched = patch_html(content, figures)
    style_old = (
        "  .shot { background: #e8e8e8; border: 2px dashed #888; min-height: 140px; display: flex; align-items: center; justify-content: center;\n"
        "    text-align: center; padding: 16px; margin: 10px 0; font-size: 9pt; color: #333; }\n"
        "  .shot small { display: block; margin-top: 8px; color: #555; font-family: ui-monospace, monospace; font-size: 8pt; }"
    )
    style_new = (
        "  .shot { margin: 10px 0; border: 1px solid #bfbfbf; background: #fafafa; padding: 0; overflow: hidden; }\n"
        "  .shot img { display: block; width: 100%; height: auto; vertical-align: middle; }\n"
        "  .shot figcaption { font-size: 8.5pt; color: #555; padding: 8px 10px; border-top: 1px solid #e5e7eb; background: #f9fafb; }"
    )
    patched = patched.replace(style_old, style_new)
    patched = patched.replace(
        "Placeholders below; capture to <code>cjb-scrawler/screenshots/run-2026-05-26/{step_id}.png</code>",
        "Annotated figures below (SVG); optional live PNG capture to <code>cjb-marketer-audit/images/{step_id}.png</code>",
    )
    patched = patched.replace(
        "add PNGs under <code>../cjb-scrawler/screenshots/run-2026-05-26/{step_id}.png</code>",
        "replace SVG with PNG in <code>cjb-marketer-audit/images/</code> after a live capture pass",
    )
    HTML.write_text(patched, encoding="utf-8")
    print(f"Wrote {len(figures)} SVGs to {OUT} and patched {HTML.name}")


if __name__ == "__main__":
    main()
