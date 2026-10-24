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
