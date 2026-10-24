#!/usr/bin/env python3
"""Elegant, readable Armenian typography for Rose & Co.

Executed after the normal website, SEO, motion, and bloom generators.
Only Armenian-language pages receive styling overrides; other languages and
all images, prices, product labels and page interactions stay unchanged.
"""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
css_file = root / "assets" / "styles.css"
assert css_file.is_file(), css_file

marker = "/* ROSE-CO-ARMENIAN-TYPOGRAPHY-v1 */"
css = css_file.read_text(encoding="utf-8")
if "family=Noto+Serif+Armenian" not in css:
    # One combined Google Fonts request instead of another blocking @import.
    anchor = "&family=Playfair+Display"
    if anchor not in css:
        raise RuntimeError("Unexpected base font import in styles.css")
    css = css.replace(
        anchor,
        "&family=Noto+Serif+Armenian:wght@400;500;600" + anchor,
        1,
    )

if marker not in css:
    css += r'''

/* ROSE-CO-ARMENIAN-TYPOGRAPHY-v1 */
/* Elegant Armenian letterforms without changing the English/Russian identity. */
html[lang="hy"] {
  --arm-serif: 'Noto Serif Armenian', 'Noto Sans Armenian', Georgia, serif;
  --arm-sans: 'Noto Sans Armenian', 'DM Sans', system-ui, sans-serif;
}
html[lang="hy"] body,
html[lang="hy"] input,
html[lang="hy"] button,
html[lang="hy"] textarea,
html[lang="hy"] select {
  font-family: var(--arm-sans);
}

/* Display typography: sculpted letterforms, open lines, no extreme tracking. */
html[lang="hy"] h1,
html[lang="hy"] h2,
html[lang="hy"] h3,
html[lang="hy"] .seo-section-title,
html[lang="hy"] .seo-article-h2,
html[lang="hy"] .seo-article-h3 {
  font-family: var(--arm-serif);
  font-weight: 500;
  letter-spacing: -.018em;
  overflow-wrap: break-word;
  hyphens: none;
}
html[lang="hy"] .hero h1 {
  font-size: clamp(39px, 4.7vw, 68px);
  line-height: 1.29;
  letter-spacing: -.023em;
  max-width: 690px;
  text-wrap: balance;
}
html[lang="hy"] .page-intro h1,
html[lang="hy"] .article-hero h1 {
  line-height: 1.27;
  letter-spacing: -.022em;
  text-wrap: balance;
}
html[lang="hy"] .section-head h2,
html[lang="hy"] .contact-section h2,
html[lang="hy"] .spotlight-copy h2 {
  line-height: 1.34;
  letter-spacing: -.019em;
  text-wrap: balance;
}
html[lang="hy"] .section-head h2 {
  font-size: clamp(30px, 3.15vw, 47px);
}
html[lang="hy"] .spotlight-copy h2,
html[lang="hy"] .contact-section h2 {
  font-size: clamp(34px, 3.4vw, 50px);
}
html[lang="hy"] .product-meta h3 {
  font-family: var(--arm-serif);
  font-weight: 500;
  font-size: 20px;
  line-height: 1.42;
  letter-spacing: -.012em;
  min-height: 2.85em;
}
html[lang="hy"] .journal-card h3,
html[lang="hy"] .seo-section-title,
html[lang="hy"] .article-body h2,
html[lang="hy"] .article-body h3 {
  font-family: var(--arm-serif);
  line-height: 1.42;
  letter-spacing: -.012em;
}

/* Body copy and actions should remain crisp on iPhones. */
html[lang="hy"] p,
html[lang="hy"] li,
html[lang="hy"] .nav-link,
html[lang="hy"] .filter-chip,
html[lang="hy"] .type-chip,
html[lang="hy"] .card-action,
html[lang="hy"] .category-label,
html[lang="hy"] .occasion-caption,
html[lang="hy"] .button,
html[lang="hy"] .article-back,
html[lang="hy"] .journal-read {
  font-family: var(--arm-sans);
}
html[lang="hy"] .hero-copy > p,
html[lang="hy"] .section-head p,
html[lang="hy"] .page-intro p,
html[lang="hy"] .article-hero > p {
  line-height: 1.9;
}
html[lang="hy"] .article-body {
  font-family: var(--arm-sans);
  line-height: 2.05;
}
html[lang="hy"] .nav-link,
html[lang="hy"] .filter-chip,
html[lang="hy"] .type-chip,
html[lang="hy"] .category-label {
  letter-spacing: .008em;
}
html[lang="hy"] .eyebrow {
  /* The English decorative micro-labels retain their original tracked type. */
  letter-spacing: .22em;
}
html[lang="hy"] .footer h4 {
  font-family: var(--arm-serif);
  font-weight: 500;
}
/* English ROSE & CO lettering keeps its original, unchanged typography. */

/* Responsive, long Armenian headings stay inside the available space. */
@media (max-width: 960px) {
  html[lang="hy"] .hero h1 { font-size: clamp(37px, 5vw, 56px); }
}
@media (max-width: 640px) {
  html[lang="hy"] .hero h1 {
    font-size: clamp(34px, 8.6vw, 51px);
    line-height: 1.32;
  }
  html[lang="hy"] .page-intro h1,
  html[lang="hy"] .article-hero h1 {
    font-size: clamp(34px, 8.7vw, 51px);
    line-height: 1.34;
  }
  html[lang="hy"] .section-head h2 {
    font-size: clamp(29px, 7vw, 38px);
    line-height: 1.37;
  }
  html[lang="hy"] .product-meta h3 {
    font-size: 16px;
    min-height: 2.85em;
    line-height: 1.43;
  }
  html[lang="hy"] .journal-card h3 {
    font-size: 23px;
    line-height: 1.39;
  }
  html[lang="hy"] .spotlight-copy h2,
  html[lang="hy"] .contact-section h2 {
    font-size: clamp(32px, 8vw, 40px);
  }
}
@media (max-width: 380px) {
  html[lang="hy"] .hero h1 { font-size: clamp(32px, 8.4vw, 41px); }
  html[lang="hy"] .product-meta h3 { font-size: 15px; }
}
'''
css_file.write_text(css, encoding="utf-8")

# The entry animation uses its own CSS file with font shorthand.
intro_css = root / "assets" / "bloom-intro.css"
if intro_css.is_file():
    value = intro_css.read_text(encoding="utf-8")
    if marker not in value:
        value += r'''

/* ROSE-CO-ARMENIAN-TYPOGRAPHY-v1 */
html[lang="hy"] .rose-bloom-caption {
  font-family: 'Noto Serif Armenian','Noto Sans Armenian',Georgia,serif;
  font-weight: 500;
  letter-spacing: -.012em;
  line-height: 1.5;
}
html[lang="hy"] .rose-bloom-skip {
  font-family: 'Noto Sans Armenian',system-ui,sans-serif;
}
'''
        intro_css.write_text(value, encoding="utf-8")

# Apply cache busting and font preconnect only to Armenian pages.
changed = 0
for path in (root / "hy").rglob("*.html"):
    html = path.read_text(encoding="utf-8")
    if 'lang="hy"' not in html[:1200]:
        continue
    html = re.sub(
        r'(/rose-and-co/assets/styles\.css)(?:\?v=[^"\']+)?',
        r'\1?v=armenian1', html,
    )
    if "fonts.gstatic.com" not in html:
        html = html.replace(
            "</head>",
            '<link rel="preconnect" href="https://fonts.googleapis.com"/>'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>'
            "</head>", 1,
        )
    if "bloom-intro.css?v=" in html:
        html = html.replace("bloom-intro.css?v=bloom1", "bloom-intro.css?v=armenian1")
    path.write_text(html, encoding="utf-8")
    changed += 1

if not changed:
    raise RuntimeError("No Armenian pages found for typography update")
print(f"Rose & Co: new Armenian serif headings + readable sans across {changed} pages")
