#!/usr/bin/env python3
"""Final Armenian type system for Rose & Co's 78-page trilingual website.

This runs *last*, after all feature CSS has been installed and after the
site's canonical/hreflang normalization. It affects only hy pages and keeps
English brand art as-is. Existing Google Fonts @import includes both families.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import re

site=Path(sys.argv[1]).resolve()
assets=site/"assets"
assert (assets/"styles.css").is_file()
font_css=(assets/"styles.css").read_text(encoding="utf-8")
assert "family=Noto+Serif+Armenian" in font_css
assert "family=Noto+Sans+Armenian" in font_css

version="hy-type-final-20261025-v1"
typography=r'''
/* ROSE-CO-FINAL-ARMENIAN-ELEGANCE-20261025
   Display: Noto Serif Armenian 500. Reading: Noto Sans Armenian 400/500.
   No forced Latin letter-spacing or tight line-height for Armenian glyphs.
*/
html[lang="hy"] {
  --hy-display:"Noto Serif Armenian","Noto Sans Armenian",serif;
  --hy-text:"Noto Sans Armenian",system-ui,-apple-system,sans-serif;
  --hy-ink:#4c2738;
  --hy-text-muted:#735f68;
  text-rendering:optimizeLegibility;
  -webkit-font-smoothing:antialiased;
}
html[lang="hy"] body {
  font-family:var(--hy-text);
  font-weight:400;
  font-size:15px;
  line-height:1.85;
  letter-spacing:0;
}
html[lang="hy"] :is(
  h1,h2,h3,h4,
  .seo-section-title,.seo-article-h2,.seo-article-h3,
  .hero h1,.page-intro h1,.article-hero h1,
  .section-head h2,.spotlight-copy h2,.contact-section h2,
  .rose-builder-header h2,.rose-builder-preview h3,
  .rs-header h2,.rs-cardhead h3,.rs-feebox strong,
  .rs-editorial-heading,.rs-result strong,
  .rs-envelopebox h4,.rs-paper p,.journal-card h3,.product-meta h3
) {
  font-family:var(--hy-display);
  font-weight:500;
  letter-spacing:0;
  font-optical-sizing:auto;
  font-kerning:normal;
  hyphens:none;
  text-wrap:pretty;
  overflow-wrap:break-word;
}
html[lang="hy"] :is(
  .hero h1,.page-intro h1,.article-hero h1,
  .section-head h2,.spotlight-copy h2,
  .rose-builder-header h2,.rs-header h2
) {text-wrap:balance;}

html[lang="hy"] :is(
  .hero h1,.page-intro h1,.article-hero h1
) {
  color:#622a42;
  line-height:1.43;
  letter-spacing:-.004em;
}
html[lang="hy"] .hero h1 {
  font-size:clamp(39px,4.3vw,64px);
  line-height:1.40;
  max-width:700px;
  margin-top:22px;
  margin-bottom:24px;
}
html[lang="hy"] .page-intro h1 {
  font-size:clamp(36px,4.6vw,57px);
  line-height:1.40;
}
html[lang="hy"] .article-hero h1 {
  font-size:clamp(35px,4.3vw,55px);
  line-height:1.40;
}
html[lang="hy"] :is(
  .section-head h2,.spotlight-copy h2,.contact-section h2,
  .rose-builder-header h2,.rs-header h2,.rs-cardhead h3
) {line-height:1.43;letter-spacing:0;}
html[lang="hy"] .section-head h2{font-size:clamp(30px,3.2vw,44px);}
html[lang="hy"] .spotlight-copy h2,
html[lang="hy"] .contact-section h2{font-size:clamp(31px,3.35vw,45px);}
html[lang="hy"] .rose-builder-header h2,
html[lang="hy"] .rs-header h2{font-size:clamp(30px,3.45vw,45px);}
html[lang="hy"] .rs-cardhead h3{font-size:clamp(25px,2.8vw,36px);}
html[lang="hy"] .product-meta h3{
  font-size:clamp(17px,1.6vw,20px);
  line-height:1.52;
  min-height:2.9em;
  margin-bottom:12px;
}
html[lang="hy"] .journal-card h3{font-size:clamp(20px,2.1vw,25px);line-height:1.48;}
html[lang="hy"] :is(.article-body h2,.seo-article-h2){line-height:1.5;}
html[lang="hy"] :is(.article-body h3,.seo-article-h3){line-height:1.5;}
html[lang="hy"] .rs-editorial-heading{font-size:clamp(19px,2vw,26px);line-height:1.5;}
html[lang="hy"] .rs-feebox strong{line-height:1.5;}
html[lang="hy"] .rose-builder-preview h3{line-height:1.5;}
html[lang="hy"] .rs-paper p{font-size:14px;line-height:2;}

/* Controls and long-form reading: consistently use the same Armenian sans. */
html[lang="hy"] :is(
  button,input,textarea,select,option,legend,label,
  p,li,blockquote,summary,small,
  .nav-link,.mobile-menu a,.footer a,
  .product-meta p,.card-action,.category-label,
  .journal-card p,.journal-read,.article-body,
  .article-back,.filter-chip,.type-chip,
  .rs-form,.rs-form label,.rs-form :is(input,select,textarea),
  .rs-textbtn,.rs-links a,.rs-sample-card p,.rs-sample-card strong,
  .rose-builder-form,.rose-builder-choice span,.rose-builder-fieldset legend,
  .rose-builder-label,.rose-builder-summary,.rose-builder-previewnote,
  .rose-builder-disclaimer,.rose-builder-order,.button,.text-link
) {font-family:var(--hy-text);}
html[lang="hy"] :is(
  .hero-copy>p,.page-intro p,.article-hero>p,.section-head p,
  .spotlight-copy p,.contact-section p,.rs-header p,.rs-cardhead p,
  .rose-builder-header p,.rose-builder-summary
) {line-height:1.9;letter-spacing:0;}
html[lang="hy"] .article-body{font-size:15px;line-height:2.0;}
html[lang="hy"] .article-body p{line-height:2.0;}
html[lang="hy"] :is(.rs-form label,.rose-builder-fieldset legend,.rose-builder-label){
  font-size:13px;
  font-weight:600;
  line-height:1.65;
  letter-spacing:0;
}
html[lang="hy"] :is(.rs-form input,.rs-form select,.rs-form textarea,
                    .rose-builder-note,.rose-builder-count){
  font-family:var(--hy-text);
  font-size:14px;
  line-height:1.62;
}
html[lang="hy"] :is(.rs-links a,.rs-textbtn,.rose-builder-choice span){
  font-family:var(--hy-text);
  font-size:13px;
  line-height:1.6;
  letter-spacing:0;
}
html[lang="hy"] :is(.button,.rose-builder-order,.rs-actions .button,
                   .nav-link,.card-action,.text-link){
  font-family:var(--hy-text);
  font-size:13px;
  font-weight:600;
  line-height:1.55;
  letter-spacing:0;
}
html[lang="hy"] :is(.rs-sample-card p,.rs-review p){
  font-family:var(--hy-text);
  font-size:13px;
  line-height:1.85;
}
html[lang="hy"] :is(.rs-editorial-notice,.rs-header p,.rose-builder-header p){
  font-family:var(--hy-text);
  font-size:13px;
  line-height:1.85;
}
html[lang="hy"] :is(.rs-sample-card strong,.rs-review strong){
  font-size:12px;
  font-weight:600;
}
html[lang="hy"] :is(.notice-strip,.marquee,.eyebrow,.brand-type,.brand-type small,
                   .rose-bloom-brand,.hero-watermark) {
  /* Roman logotype and editorial English microtype deliberately retain their
     existing appearance, rather than being forced into an Armenian fallback. */
}
html[lang="hy"] .brand-type{font-family:Georgia,serif;}
html[lang="hy"] .brand-type small{font-family:"DM Sans",system-ui,sans-serif;}
html[lang="hy"] .rose-bloom-caption {
  font-family:var(--hy-display);
  font-weight:500;
  line-height:1.62;
  letter-spacing:0;
}
html[lang="hy"] .rose-bloom-skip{
  font-family:var(--hy-text);
  font-weight:600;
  letter-spacing:0;
}
@media(max-width:960px){
 html[lang="hy"] .hero h1{font-size:clamp(36px,4.5vw,52px);line-height:1.41;}
}
@media(max-width:640px){
 html[lang="hy"] body{font-size:14px;line-height:1.82}
 html[lang="hy"] .hero h1{font-size:clamp(32px,8.3vw,42px);line-height:1.47;}
 html[lang="hy"] .page-intro h1,
 html[lang="hy"] .article-hero h1{font-size:clamp(30px,7.8vw,39px);line-height:1.5;}
 html[lang="hy"] .section-head h2{font-size:clamp(27px,7vw,34px);line-height:1.48;}
 html[lang="hy"] .rs-header h2,
 html[lang="hy"] .rose-builder-header h2{font-size:clamp(28px,7vw,36px);line-height:1.48;}
 html[lang="hy"] .rs-cardhead h3{font-size:clamp(24px,6.3vw,30px);line-height:1.47;}
 html[lang="hy"] .spotlight-copy h2,
 html[lang="hy"] .contact-section h2{font-size:clamp(29px,7.1vw,36px);line-height:1.48;}
 html[lang="hy"] .journal-card h3{font-size:21px;line-height:1.5;}
 html[lang="hy"] .product-meta h3{font-size:17px;min-height:2.9em}
 html[lang="hy"] :is(.rs-form input,.rs-form select,.rs-form textarea,
                      .rose-builder-note,.rose-builder-count){font-size:16px;}
 html[lang="hy"] .hero-buttons{gap:12px 16px;}
 html[lang="hy"] .hero-buttons .text-link{font-size:12px;line-height:1.55;}
 html[lang="hy"] .rs-card,.rose-builder-form{overflow-wrap:break-word;}
}
@media(max-width:360px) {
 html[lang="hy"] .hero h1{font-size:31px;}
 html[lang="hy"] .page-intro h1{font-size:29px;}
 html[lang="hy"] .section-head h2{font-size:27px;}
 html[lang="hy"] .rs-header h2{font-size:27px;}
 html[lang="hy"] .rs-cardhead h3{font-size:23px;}
}
'''
path=assets/"armenian-elegance.css"
path.write_text(typography+"\n",encoding="utf-8")

count=0
for file in (site/"hy").rglob("*.html"):
    src=file.read_text(encoding="utf-8")
    assert "</head>" in src and 'lang="hy"' in src[:1000],file
    assert "armenian-elegance.css" not in src,file
    src=src.replace("</head>",f'<link rel="stylesheet" href="/rose-and-co/assets/armenian-elegance.css?v={version}"/></head>',1)
    file.write_text(src,encoding="utf-8")
    count+=1
assert count==32,f"Expected 32 Armenian pages, got {count}"
assert "armenian-elegance.css" not in (site/"ru"/"index.html").read_text(encoding="utf-8")
assert "armenian-elegance.css" not in (site/"en"/"index.html").read_text(encoding="utf-8")
print(f"Rose & Co Armenian premium typography applied to {count} Armenian pages; no RU/EN changes.")
