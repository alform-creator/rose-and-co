#!/usr/bin/env python3
"""Add the approved second circular R ✧ CO seal to Rose & Co's story section.

The extra lower-left circle echoes the supplied mobile screenshot. Keep the
existing top-right floral badge, real photos and accessible story copy intact.
Run last, after install-story-decor.py, to preserve the intended layout.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re, sys

root=Path(sys.argv[1]).resolve()
assets=root/"assets"
logo_svg = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="180" height="180" aria-hidden="true">
  <title>Rose and Co monogram</title>
  <defs>
    <radialGradient id="paper" cx=".35" cy=".24" r=".95">
      <stop stop-color="#fffdf8"/>
      <stop offset="1" stop-color="#f6ebe5"/>
    </radialGradient>
  </defs>
  <circle cx="90" cy="90" r="85.5" fill="url(#paper)" stroke="#692c42" stroke-width="2"/>
  <g transform="translate(90 92) rotate(9)" fill="#6a2d42">
    <text x="-63" y="11" font-size="48" font-style="italic" font-family="Georgia, 'Times New Roman',serif">R</text>
    <path d="M-15 -2 L-8 1 L-5 10 L-2 1 L5 -2 L-2 -5 L-5 -14 L-8 -5 Z"
          transform="translate(-2,-2) scale(.92)" fill="none" stroke="#b59872" stroke-width="2" stroke-linejoin="round"/>
    <text x="13" y="11" font-size="41" letter-spacing="-2.2" font-family="Georgia, 'Times New Roman',serif">CO</text>
  </g>
</svg>'''
(assets/"story-rc-monogram.svg").write_text(logo_svg+"\n",encoding="utf-8")

counter=0
for lang in ("hy","ru","en"):
  for page in (root/lang).rglob("*.html"):
    html=page.read_text(encoding="utf-8")
    if "about-spotlight" not in html:
      continue
    soup=BeautifulSoup(html,"html.parser")
    for gallery in soup.select(".about-spotlight .spotlight-gallery"):
      if gallery.select_one(".story-secondary-monogram"):
        continue
      node=soup.new_tag("span")
      node["class"]=["story-secondary-monogram"]
      node["aria-hidden"]="true"
      image=soup.new_tag("img",alt="",src="/rose-and-co/assets/story-rc-monogram.svg?v=story-monogram1",width="140",height="140",decoding="async")
      node.append(image)
      gallery.append(node)
      counter+=1
    page.write_text(str(soup),encoding="utf-8")

if counter!=6:
  raise RuntimeError(f"Expected 6 story galleries on HY/RU/EN home + about, got {counter}")

css_path=assets/"styles.css"
css=css_path.read_text(encoding="utf-8")
marker="/* ROSE-CO-STORY-SECOND-MONOGRAM-v1 */"
if marker not in css:
  css+=r'''

/* ROSE-CO-STORY-SECOND-MONOGRAM-v1 */
/* The small R ✧ CO signet on the lower-left, paired with the rose signet above. */
.about-spotlight .story-secondary-monogram {
  position:absolute;
  left:-20px;
  bottom:64px;
  z-index:5;
  width:clamp(100px,11vw,140px);
  aspect-ratio:1/1;
  display:block;
  pointer-events:none;
  transform:rotate(-9deg);
  filter:drop-shadow(0 8px 15px rgba(95,41,62,.13));
}
.story-secondary-monogram img {
  display:block;
  width:100%;
  height:100%;
  object-fit:contain;
}
@media (max-width:960px) {
  .about-spotlight .story-secondary-monogram {
    width:106px;
    bottom:49px;
    left:-14px;
  }
}
@media (max-width:640px) {
  .about-spotlight .story-secondary-monogram {
    width:100px;
    left:-9px;
    bottom:14px;
  }
}
@media (max-width:380px) {
  .about-spotlight .story-secondary-monogram {
    width:84px;
    left:-6px;
    bottom:14px;
  }
}
@media (prefers-reduced-motion:no-preference) and (hover:hover) {
  .story-secondary-monogram { transition:transform .7s cubic-bezier(.22,1,.36,1); }
  .spotlight-gallery:hover .story-secondary-monogram {
    transform:rotate(-3deg) translateY(-3px);
  }
}
@media (prefers-reduced-motion:reduce) {
  .story-secondary-monogram {transition:none!important;}
}
'''
  css_path.write_text(css,encoding="utf-8")

# Bust stale mobile Safari styles after the new mark is installed.
for page in root.rglob("*.html"):
  html=page.read_text(encoding="utf-8")
  html=re.sub(r'(/rose-and-co/assets/styles\.css)(?:\?v=[^"\']+)?',
              r'\1?v=story-monogram1',html)
  page.write_text(html,encoding="utf-8")
print(f"Rose & Co: second R ✧ CO story seal installed on {counter} HY/RU/EN sections.")


# ROSE-CO-LUXURY-UNIFIED-BACKGROUNDS-20261025
# Carry the beloved story-section blush and botanical flourishes throughout
# the entire site. Purely presentational: do not touch text, links or photos.
# Derived from the story floral artwork, with a gentle opacity for readability.
spray_source=(assets/"story-floral-spray.svg").read_text(encoding="utf-8")
if "<svg " not in spray_source:
    raise RuntimeError("Story floral artwork is missing")
light_spray=spray_source.replace("<svg ", '<svg opacity=".27" ', 1)
(assets/"rose-atelier-soft-floral.svg").write_text(light_spray, encoding="utf-8")
gold_spray=spray_source
for original, replacement in {
    "#8eaa87":"#e4ceb4",
    "#6b8070":"#b7a08a",
    "#759277":"#d8baa4",
    "#ffe3e1":"#f5e1da",
    "#db9da7":"#e5bcb6",
    "#c17e8e":"#d8a99f",
    "#f5c3c4":"#f2d3c9",
    "#f2b8c0":"#eed0c8",
    "#a56477":"#a87d71",
    "#b16f81":"#a87d71",
}.items():
    gold_spray=gold_spray.replace(original, replacement)
gold_spray=gold_spray.replace("<svg ", '<svg opacity=".33" ', 1)
(assets/"rose-atelier-gold-floral.svg").write_text(gold_spray, encoding="utf-8")

luxury_css=r'''

/* ROSE-CO-LUXURY-UNIFIED-BACKGROUNDS-20261025 */
/* The "Our Story" rose/cream palette now flows through EVERY site section.
   Floral ornaments live behind content, without obscuring product images. */
:root {
  --rose-atelier-silk: #fcf7f3;
  --rose-atelier-blush: #f5e6e3;
  --rose-atelier-champagne: #e4d0bd;
  --rose-atelier-floral: url("/rose-and-co/assets/rose-atelier-soft-floral.svg?v=luxe1");
  --rose-atelier-gold: url("/rose-and-co/assets/rose-atelier-gold-floral.svg?v=luxe1");
}
body { background-color: var(--rose-atelier-silk); }
main {
  background-color:#fcf6f2;
  background-image:
    radial-gradient(ellipse at 10% 30%,rgba(235,200,199,.16),transparent 45%),
    linear-gradient(145deg,#fff9f5 0%,#fbf3ef 51%,#f8eae6 100%);
}
.site-header { background:rgba(255,249,245,.975); }
.hero {
  background-color:#f6e9e5;
  background-image:
    var(--rose-atelier-floral),
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 86% 22%,rgba(221,164,172,.32),transparent 43%),
    radial-gradient(ellipse at 5% 90%,rgba(229,198,185,.30),transparent 46%),
    linear-gradient(115deg,#fff7f2 1%,#f8ebe7 53%,#efd5d2 100%);
  background-position:left -135px bottom -170px,right -135px top -145px,center,center,center;
  background-size:clamp(230px,27vw,365px) auto,clamp(220px,26vw,355px) auto,auto,auto,auto;
  background-repeat:no-repeat;
}
.page-intro {
  background-color:#f5e6e3;
  background-image:
    var(--rose-atelier-floral),
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 80% 28%,rgba(227,182,183,.36),transparent 40%),
    linear-gradient(140deg,#fff8f3 0%,#f5e7e3 55%,#efd9d5 100%);
  background-position:left -110px top -150px,right -110px bottom -200px,center,center;
  background-size:clamp(205px,24vw,320px) auto,clamp(220px,27vw,340px) auto,auto,auto;
  background-repeat:no-repeat;
  box-shadow:inset 0 -1px rgba(160,112,118,.16);
}
.categories-section {
  background-color:#fff9f5;
  background-image:
    var(--rose-atelier-floral),
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 50% 0%,rgba(233,199,198,.22),transparent 63%),
    linear-gradient(135deg,#fffaf7,#f9efeb 70%,#fbf4ed);
  background-position:left -160px bottom -265px,right -160px top -260px,center,center;
  background-size:clamp(240px,29vw,400px) auto,clamp(240px,29vw,400px) auto,auto,auto;
  background-repeat:no-repeat;
  box-shadow:inset 0 1px rgba(173,122,130,.12),inset 0 -1px rgba(173,122,130,.12);
}
/* The full-bleed underlay keeps container-width sections visually continuous. */
main > section.section.container {
  position:relative;
  isolation:isolate;
}
main > section.section.container::before {
  content:"";
  pointer-events:none;
  position:absolute;
  z-index:-1;
  top:0;
  bottom:0;
  left:50%;
  width:100vw;
  transform:translateX(-50%);
  background-color:#fbf3ef;
  background-image:
    var(--rose-atelier-floral),
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 75% 18%,rgba(227,189,189,.22),transparent 55%),
    linear-gradient(155deg,#fff9f5 0%,#faf0ed 55%,#f7e8e4 100%);
  background-position:left -175px bottom -250px,right -170px top -220px,center,center;
  background-size:clamp(240px,30vw,410px) auto,clamp(240px,29vw,390px) auto,auto,auto;
  background-repeat:no-repeat;
  box-shadow:inset 0 -1px rgba(177,125,134,.10);
}
main > section.section.container:nth-of-type(even)::before {
  background-position:left -140px top -255px,right -165px bottom -260px,center,center;
  background-image:
    var(--rose-atelier-floral),
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 18% 80%,rgba(223,182,181,.24),transparent 51%),
    linear-gradient(25deg,#f9eee9 0%,#fff9f5 56%,#f5e5e0 100%);
}
.about-spotlight {
  background-color:#f2dfdb;
  background-image:
    radial-gradient(ellipse at 12% 15%,rgba(255,250,244,.72),transparent 52%),
    radial-gradient(ellipse at 88% 76%,rgba(226,170,179,.27),transparent 43%),
    linear-gradient(137deg,#f9eee9 0%,#f1dedb 51%,#f7e7e3 100%);
  box-shadow:inset 0 1px rgba(158,101,115,.14),inset 0 -1px rgba(158,101,115,.15);
}
.about-spotlight::before { opacity:.38; }
.about-spotlight::after { opacity:.26; }
.contact-section {
  background-color:#421827;
  background-image:
    var(--rose-atelier-gold),
    var(--rose-atelier-gold),
    radial-gradient(ellipse at 78% 13%,rgba(160,88,110,.31),transparent 49%),
    radial-gradient(ellipse at 14% 85%,rgba(158,99,99,.20),transparent 50%),
    linear-gradient(145deg,#351320 0%,#54233a 55%,#3e1726 100%);
  background-position:left -125px bottom -190px,right -120px top -160px,center,center,center;
  background-size:clamp(230px,25vw,345px) auto,clamp(230px,25vw,345px) auto,auto,auto,auto;
  background-repeat:no-repeat;
  box-shadow:inset 0 1px rgba(237,208,178,.18),inset 0 -1px rgba(237,208,178,.17);
}
.footer {
  background-color:#f9ede8;
  background-image:
    var(--rose-atelier-floral),
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 50% 0%,rgba(234,195,196,.23),transparent 65%),
    linear-gradient(120deg,#fff9f5,#f6e8e4 60%,#fff8f2);
  background-position:left -160px bottom -235px,right -190px top -250px,center,center;
  background-size:clamp(230px,27vw,360px) auto,clamp(235px,27vw,365px) auto,auto,auto;
  background-repeat:no-repeat;
}
.article-hero, .article-body, .article-return {
  position:relative;
  isolation:isolate;
}
.article-hero::before {
  content:"";
  pointer-events:none;
  position:absolute;
  z-index:-1;
  top:0;
  bottom:0;
  left:50%;
  width:100vw;
  transform:translateX(-50%);
  background-image:
    var(--rose-atelier-floral),
    radial-gradient(ellipse at 70% 30%,rgba(231,196,192,.20),transparent 60%),
    linear-gradient(140deg,#fff9f6,#f7eae6);
  background-size:clamp(200px,26vw,345px) auto,auto,auto;
  background-position:left -125px top -155px,center,center;
  background-repeat:no-repeat;
}
@media (max-width:640px) {
  .hero {
    background-position:left -75px bottom -95px,right -95px top -135px,center,center,center;
    background-size:150px auto,155px auto,auto,auto,auto;
  }
  .page-intro {
    background-position:left -95px top -165px,right -80px bottom -195px,center,center;
    background-size:155px auto,150px auto,auto,auto;
  }
  .categories-section {
    background-position:left -112px bottom -190px,right -120px top -245px,center,center;
    background-size:185px auto,175px auto,auto,auto;
  }
  main > section.section.container::before,
  main > section.section.container:nth-of-type(even)::before {
    background-position:left -125px bottom -200px,right -125px top -180px,center,center;
    background-size:175px auto,165px auto,auto,auto;
  }
  .contact-section {
    background-position:left -105px bottom -160px,right -120px top -155px,center,center,center;
    background-size:150px auto,165px auto,auto,auto,auto;
  }
  .footer {
    background-position:left -125px bottom -195px,right -125px top -170px,center,center;
    background-size:170px auto,170px auto,auto,auto;
  }
  .article-hero::before {
    background-position:left -110px top -155px,center,center;
    background-size:170px auto,auto,auto;
  }
  .about-spotlight::before { opacity:.21; }
  .about-spotlight::after { opacity:.16; }
}
'''
css_path=assets/"styles.css"
existing_css=css_path.read_text(encoding="utf-8")
if "/* ROSE-CO-LUXURY-UNIFIED-BACKGROUNDS-20261025 */" not in existing_css:
    css_path.write_text(existing_css+luxury_css, encoding="utf-8")

# A CSS cache revision is essential on Safari, where old styles often linger.
updated_pages=0
for page in root.rglob("*.html"):
    html=page.read_text(encoding="utf-8")
    refreshed=re.sub(
        r'(/rose-and-co/assets/styles\.css)(?:\?v=[^"\']+)?',
        r'\1?v=rose-luxe-20261025', html)
    if refreshed!=html:
        page.write_text(refreshed, encoding="utf-8")
        updated_pages+=1
assert updated_pages>=18, f"Expected every translated page, found {updated_pages}"
assert (assets/"rose-atelier-soft-floral.svg").exists()
assert (assets/"rose-atelier-gold-floral.svg").exists()
print(f"Rose & Co unified luxury botanical backgrounds on {updated_pages} pages.")
