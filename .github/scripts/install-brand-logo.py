#!/usr/bin/env python3
"""Add the Rose & Co premium vector rose emblem to all site wordmarks.

Replace only ornamental brand symbols (header, footer, landing intro).
Keep actual ROSE & CO lettering, SEO copy, images, and catalog untouched.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
assets = root / "assets"
assets.mkdir(parents=True, exist_ok=True)

svg = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img" aria-label="Rose &amp; Co rose emblem">
  <defs>
    <linearGradient id="rc-paper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fffdf9"/>
      <stop offset="1" stop-color="#f6e8e6"/>
    </linearGradient>
    <linearGradient id="rc-petals" x1="0" y1="0" x2=".85" y2="1">
      <stop offset="0" stop-color="#e7b9bd"/>
      <stop offset=".63" stop-color="#c87d91"/>
      <stop offset="1" stop-color="#9a4868"/>
    </linearGradient>
  </defs>
  <circle cx="48" cy="48" r="45" fill="url(#rc-paper)" stroke="#c8ae9c" stroke-width="1.3"/>
  <circle cx="48" cy="48" r="40.5" fill="none" stroke="#d8c5b8" stroke-width=".65"/>
  <g fill="none" stroke="#b69d8b" stroke-width="1" stroke-linecap="round" opacity=".8">
    <path d="M13 48h5M78 48h5"/>
    <path d="M48 11v5M48 80v5"/>
  </g>
  <!-- Living stem and two soft botanical leaves -->
  <path d="M47.8 54.7 C46.8 61.8 49.4 70 48.4 78.2" fill="none" stroke="#617963" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M47.7 70.1 C40 59.9 31 60.3 25.2 63.9 C30.7 72.2 39.8 74.4 47.7 70.1Z"
        fill="#91a792" fill-opacity=".78" stroke="#506b58" stroke-width="1.15" stroke-linejoin="round"/>
  <path d="M48.8 64.5 C56.6 55.4 65.8 57.7 70.1 62.2 C65.6 69.9 56.9 71.1 48.8 64.5Z"
        fill="#a4b69f" fill-opacity=".84" stroke="#56725c" stroke-width="1.15" stroke-linejoin="round"/>
  <path d="M46.2 69.8 29.3 65.1M49.7 65 66 61.7" fill="none" stroke="#f1ead8" stroke-width="1" opacity=".85"/>
  <!-- Five soft outer petals of an open rose -->
  <g stroke="#884359" stroke-width="1.35" stroke-linejoin="round" fill="url(#rc-petals)">
    <path d="M48.8 23.2 C39.5 16.1 31.1 24.8 33.2 35 C27 29.8 18.8 34.7 21.4 44.5 C23.9 51.7 30.7 56.6 39.1 54.6 C40.3 63.1 50 66.3 56.5 59.2 C64.3 64.2 73.2 55.8 70.9 47.4 C80.4 40.1 71.4 29.6 63.3 32.6 C60.7 22.1 53.8 20 48.8 23.2Z"/>
  </g>
  <!-- The inner folds give the rose a natural, hand-engraved look -->
  <g fill="none" stroke="#73334d" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M33.4 35.4 C36.4 29.3 42.9 27.9 48.4 31.2 C55 25.7 62.5 30.1 63.1 36.1"/>
    <path d="M28.6 42.3 C30.4 49.7 36.2 53.5 42.6 50.3"/>
    <path d="M66.8 40.8 C67.3 48.4 63.2 52.6 56.9 52"/>
    <path d="M40.5 53.2 C45.1 58.3 51.4 58.2 56.7 52.2"/>
    <path d="M39.6 38.8 C42.7 33.1 52.4 33.2 56.1 39.8 C60.1 47.5 53.5 52.5 47.8 51.1 C42.3 49.4 42.6 42.1 47 40.1 C50.9 38.5 53.2 42 50.5 44.6"/>
  </g>
  <path d="M34 30.2C34.8 25.7 39.5 22.6 44.2 24.8" fill="none" stroke="#fff1e8" stroke-width="1.4" stroke-linecap="round" opacity=".8"/>
  <path d="M58.8 33.8C62.7 32 67.5 34.8 67.4 39.3" fill="none" stroke="#f9dadb" stroke-width="1.25" stroke-linecap="round" opacity=".8"/>
</svg>'''
(assets / "brand-rose.svg").write_text(svg + "\n", encoding="utf-8")
# Browser tab icon and on-page logo use the same family of marks.
(assets / "mark.svg").write_text(svg + "\n", encoding="utf-8")

img = '<img class="brand-rose-mark" src="/rose-and-co/assets/brand-rose.svg?v=brand1" alt="" aria-hidden="true" width="52" height="52" decoding="async"/>'
intro_img = '<img class="rose-bloom-logo" src="/rose-and-co/assets/brand-rose.svg?v=brand1" alt="" width="34" height="34" decoding="async"/>'
changed = 0
logos_replaced = 0
intro_replaced = 0
for lang in ("hy", "ru", "en"):
    for page in (root / lang).rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        original = html
        # Supports compact and BeautifulSoup-normalized markup.
        html, count = re.subn(
            r'<span\s+class=["\']brand-emblem["\']\s*>\s*❀\s*</span>',
            img, html,
        )
        logos_replaced += count
        # The splash intro appears on each language home page only.
        html, count = re.subn(
            r'(<div\s+class=["\']rose-bloom-brand["\']\s+aria-hidden=["\']true["\']\s*>)',
            lambda m: m.group(1) + intro_img,
            html,
        )
        intro_replaced += count
        if html != original:
            page.write_text(html, encoding="utf-8")
            changed += 1

if logos_replaced < 18 or intro_replaced != 3:
    raise RuntimeError(f"Unexpected brand HTML: {logos_replaced} emblems, {intro_replaced} intros")
css_file = assets / "styles.css"
css = css_file.read_text(encoding="utf-8")
marker = "/* ROSE-CO-PREMIUM-BRAND-v1 */"
if marker not in css:
    css += r'''
/* ROSE-CO-PREMIUM-BRAND-v1: line-drawn rose + refined ROSE & CO wordmark. */
.brand { gap: 11px; align-items:center; }
.brand-rose-mark {
  flex: none; display:block; object-fit: contain;
  width: 52px; height: 52px;
  filter: drop-shadow(0 3px 3px rgba(89,40,57,.05));
  transition: transform .55s cubic-bezier(.22, 1, .36, 1), filter .4s ease;
}
.brand-type {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 25px;
  font-weight: 500;
  letter-spacing: .075em;
  line-height: 1.02;
  white-space: nowrap;
}
.brand-type i { color: #af8291; font-size:.74em; }
.brand-type small {
  display: block;
  font-family: 'DM Sans', 'Noto Sans Armenian', system-ui, sans-serif;
  font-weight: 600;
  font-size: 8px;
  letter-spacing: .27em;
  line-height: 1.4;
  margin-top: 9px;
}
.footer-brand .brand-rose-mark { width: 58px; height:58px; }
@media (hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference) {
  .brand:hover .brand-rose-mark,
  .brand:focus-visible .brand-rose-mark {
    transform: rotate(-7deg) scale(1.035);
    filter: drop-shadow(0 5px 7px rgba(89,40,57,.13));
  }
}
.rose-bloom-brand {
  display:flex; align-items:center; justify-content:center;
  gap:11px; font-family:'Playfair Display',Georgia,serif;
  letter-spacing:.18em;
}
.rose-bloom-brand .rose-bloom-logo {
  width:34px;height:34px;flex:none;display:block;object-fit:contain;
  filter:drop-shadow(0 4px 6px rgba(104,52,73,.1));
}
@media (max-width: 960px) {
  .site-header .brand-rose-mark { width:43px;height:43px; }
  .site-header .brand-type { font-size:22px; }
}
@media (max-width: 640px) {
  .site-header .brand { gap:7px; }
  .site-header .brand-rose-mark { width:35px;height:35px; }
  .site-header .brand-type { font-size:19px; letter-spacing:.06em; }
  .site-header .brand-type small { font-size:6.5px;letter-spacing:.18em;margin-top:6px; }
  .footer-brand .brand-rose-mark { width:47px;height:47px; }
  .footer-brand .brand-type { font-size:21px; }
  .rose-bloom-brand .rose-bloom-logo { width:29px;height:29px; }
}
@media (max-width: 380px) {
  .site-header .brand-rose-mark { width:31px;height:31px; }
  .site-header .brand-type { font-size:17px; }
}
@media (prefers-reduced-motion:reduce) {
  .brand-rose-mark { transition:none !important; transform:none !important; }
}
'''
    css_file.write_text(css, encoding="utf-8")

# Refresh CSS for branded imagery even for previously visited visitors.
for page in root.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    html = re.sub(
        r'(/rose-and-co/assets/styles\.css)(?:\?v=[^"\']+)?',
        r'\1?v=brand1',
        html,
    )
    page.write_text(html, encoding="utf-8")
print(f"Rose & Co vector rose emblem published on {changed} pages; {logos_replaced} icons plus {intro_replaced} intro marks")
