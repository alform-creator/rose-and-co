#!/usr/bin/env python3
"""Give the Rose & Co story gallery editorial botanical decoration.
Only replaces story-area decorative imagery. Original product catalogue,
hero, SEO headings, contact links and brand logo are left unchanged.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import re
import sys

root = Path(sys.argv[1]).resolve()
assets = root / "assets"
assert (assets / "styles.css").exists()

# A fine botanical rose illustration—not the old circular R / CO lettering.
# Decorative, accessible and crisp at any screen resolution.
emblem = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" width="220" height="220">
<defs>
  <radialGradient id="rose-paper" cx=".42" cy=".35" r=".81">
    <stop stop-color="#fffdf9"/><stop offset=".67" stop-color="#fcf2eb"/>
    <stop offset="1" stop-color="#e8d1cb"/>
  </radialGradient>
  <linearGradient id="rose-pink" x1="0" y1="0" x2=".9" y2="1">
    <stop stop-color="#f7d2d5"/><stop offset=".52" stop-color="#cf8e9e"/>
    <stop offset="1" stop-color="#a54d69"/>
  </linearGradient>
  <linearGradient id="rose-leaves" x1=".1" y1="0" x2=".9" y2="1">
    <stop stop-color="#7e9c7d"/><stop offset="1" stop-color="#496856"/>
  </linearGradient>
  <filter id="soft-glow"><feGaussianBlur stdDeviation="1.35"/></filter>
</defs>
<circle cx="110" cy="110" r="105" fill="url(#rose-paper)" stroke="#743449" stroke-width="1.5"/>
<circle cx="110" cy="110" r="95.5" fill="none" stroke="#c1a087" stroke-width=".85" opacity=".85"/>
<g fill="none" stroke="#7b8d76" stroke-width="2.3" stroke-linecap="round">
  <path d="M105 133 Q114 156 95 179 Q83 188 70 190"/>
  <path d="M105 154 Q125 168 143 174"/>
</g>
<g fill="url(#rose-leaves)" stroke="#6e816b" stroke-width=".7">
  <path d="M102 157 Q76 145 65 126 Q90 123 103 153Z"/>
  <path d="M105 168 Q133 137 156 145 Q148 164 107 172Z"/>
  <path d="M92 183 Q76 165 58 169 Q70 192 92 183Z"/>
  <path d="M143 173 Q154 159 176 157 Q166 174 143 173Z"/>
</g>
<g stroke="#f5d5d2" stroke-width="1" fill="none" opacity=".82">
  <path d="M101 152Q84 139 73 130"/><path d="M111 169Q134 155 148 148"/>
  <path d="M91 181Q75 176 65 172"/>
</g>
<g transform="translate(105 102)">
  <path d="M0 -43 C22 -58 38 -44 36 -26 Q58 -20 47 2 Q56 27 28 36
       Q10 58 -12 42 Q-39 47 -43 21 Q-60 -1 -36 -21 Q-38 -49 -12 -42Z"
       fill="#d99bab" stroke="#a35e73" stroke-width="1.4"/>
  <path d="M0 -42 Q24 -44 21 -17 Q45 -27 44 -3 Q48 23 19 20
       Q18 44 -5 34 Q-30 41 -31 17 Q-49 2 -24 -10 Q-31 -34 -6 -24Z"
       fill="url(#rose-pink)" stroke="#9d5571" stroke-width="1.4"/>
  <path d="M-3 -31 Q11 -39 12 -21 Q32 -27 29 -8 Q41 4 20 12
       Q24 27 7 28 Q-6 37 -17 21 Q-35 18 -24 4 Q-31 -14 -14 -17Z"
       fill="#efb5bb" stroke="#a9667a" stroke-width="1.3"/>
  <path d="M1 -23 Q15 -24 17 -10 Q30 -4 13 6 Q20 22 3 22
       Q-13 25 -16 7 Q-24 -3 -10 -10Z"
       fill="#f8d0ce" stroke="#ba7b89" stroke-width="1.5"/>
  <path d="M0 -14 Q11 -17 13 -6 Q20 6 8 12 Q-2 20 -11 9 Q-13 -3 0 -4
       Q8 -5 8 1 Q3 10 -3 6"
       fill="none" stroke="#96516b" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M-36 -20 Q-27 -41 -12 -38 M33 -24Q42 -7 39 4
       M-30 18Q-13 40 3 38" fill="none" stroke="#ffe8e2" stroke-width="2.4" opacity=".8"/>
</g>
<g fill="#b59d7a" opacity=".85">
  <circle cx="60" cy="86" r="2"/><circle cx="155" cy="70" r="1.8"/>
  <circle cx="158" cy="111" r="1.2"/><circle cx="73" cy="161" r="1.3"/>
</g>
</svg>'''

# Delicate rose sprays are decorative layers, not a duplicate logo.
spray = r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 690" width="460" height="690">
<defs>
  <linearGradient id="s-leaf" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="#8eaa87"/><stop offset="1" stop-color="#6b8070"/>
  </linearGradient>
  <linearGradient id="s-petal" x1="0" y1="0" x2="1" y2="1">
    <stop stop-color="#ffe3e1"/><stop offset=".53" stop-color="#db9da7"/>
    <stop offset="1" stop-color="#c17e8e"/>
  </linearGradient>
</defs>
<g opacity=".69" stroke="#759277" stroke-width="2.5" fill="none" stroke-linecap="round">
  <path d="M-17 401 C111 329 120 214 182 113 Q210 64 280 30"/>
  <path d="M40 364 Q113 340 189 349 Q231 356 311 311"/>
  <path d="M90 282 Q65 202 92 140"/>
  <path d="M138 194 Q196 205 232 176"/>
  <path d="M202 83 Q183 53 202 4"/>
</g>
<g fill="url(#s-leaf)" opacity=".69">
  <path d="M87 309 Q17 253 38 215 Q84 244 87 309Z"/>
  <path d="M101 292 Q136 221 186 235 Q149 282 101 292Z"/>
  <path d="M167 202 Q110 156 129 103 Q175 153 167 202Z"/>
  <path d="M183 119 Q217 72 268 83 Q243 121 183 119Z"/>
  <path d="M152 335 Q190 290 254 291 Q215 333 152 335Z"/>
  <path d="M75 361 Q34 309 -11 315 Q8 347 75 361Z"/>
</g>
<g stroke="#fcf4ef" fill="#fff8ef" opacity=".9">
  <circle cx="262" cy="48" r="4.4"/><circle cx="288" cy="28" r="3.4"/>
  <circle cx="298" cy="66" r="4.3"/><circle cx="324" cy="42" r="3.7"/>
  <circle cx="243" cy="88" r="3.5"/><circle cx="207" cy="31" r="2.8"/>
  <circle cx="183" cy="70" r="3.4"/><circle cx="319" cy="98" r="3.9"/>
  <circle cx="268" cy="115" r="3.4"/><circle cx="337" cy="62" r="2.4"/>
  <circle cx="327" cy="298" r="4.1"/><circle cx="346" cy="277" r="3.7"/>
  <circle cx="355" cy="316" r="4.5"/><circle cx="295" cy="295" r="3.5"/>
</g>
<g transform="translate(193 176) rotate(-21)">
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(0)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(60)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(120)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(180)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(240)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(300)"/>
  <circle r="26" fill="#f5c3c4"/><path d="M-14 -5 Q-11 -22 8 -14 Q23 -5 8 12 Q-9 24 -16 5 Q-19 -4 -2 -3 Q7 2 0 7" fill="none" stroke="#a56477" stroke-width="4"/>
</g>
<g transform="translate(328 305) scale(.62)">
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(0)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(72)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(144)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(216)"/>
  <ellipse cy="-33" rx="26" ry="48" fill="url(#s-petal)" transform="rotate(288)"/>
  <circle r="25" fill="#f2b8c0"/><path d="M-10 -5Q-3 -15 9 -6Q18 5 6 12Q-8 15 -12 3Q-8 -5 3 1" fill="none" stroke="#b16f81" stroke-width="4"/>
</g>
</svg>'''
(assets / "story-rose-ornament.svg").write_text(emblem + "\n", encoding="utf-8")
(assets / "story-floral-spray.svg").write_text(spray + "\n", encoding="utf-8")

# Refine the exact gallery shown in the user's screenshot, including /about/.
# Curate two different original flower photos as the editorial image pair.
names = {
  "hy": ("Գեղեցիկ վարդերի ծաղկային կոմպոզիցիա", "Նուրբ վարդագույն ծաղիկներ", "Դեկորատիվ վարդ"),
  "ru": ("Красивые розы и цветочная композиция", "Нежные розовые цветы", "Декоративная роза"),
  "en": ("Decorative rose bouquet arrangement", "Delicate pink flowers", "Decorative rose")
}
count = 0
for lang, labels in names.items():
    for page in (root / lang).rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        if "about-spotlight" not in text or "spotlight-gallery" not in text:
            continue
        soup = BeautifulSoup(text, "html.parser")
        for gallery in soup.select(".about-spotlight .spotlight-gallery"):
            large = gallery.select_one(".spotlight-large img")
            small = gallery.select_one(".spotlight-small img")
            badge = gallery.select_one(".about-stamp")
            if not (large and small and badge):
                raise RuntimeError(f"Story decor target missing from {page}")
            large["src"] = "/rose-and-co/assets/images/real-2026/flowers-02.webp?v=story-decor1"
            large["alt"] = labels[0]
            large["decoding"] = "async"
            large["loading"] = "eager"
            small["src"] = "/rose-and-co/assets/images/real-2026/flowers-35.webp?v=story-decor1"
            small["alt"] = labels[1]
            small["decoding"] = "async"
            small["loading"] = "eager"
            badge["aria-label"] = labels[2]
            badge["class"] = ["about-stamp", "about-stamp-rose", "story-floral-seal"]
            img = badge.select_one("img")
            if img is None:
                badge.clear()
                img = soup.new_tag("img")
                badge.append(img)
            img["src"] = "/rose-and-co/assets/story-rose-ornament.svg?v=story-decor1"
            img["width"] = "124"
            img["height"] = "124"
            img["alt"] = ""
            img["decoding"] = "async"
            count += 1
        page.write_text(str(soup), encoding="utf-8")

if count != 6:
    raise RuntimeError(f"Expected story gallery in home and about for 3 languages; updated {count}")

css_path = assets / "styles.css"
css = css_path.read_text(encoding="utf-8")
marker = "/* ROSE-CO-STORY-FLORAL-DECOR-1 */"
if marker not in css:
    css += r'''

/* ROSE-CO-STORY-FLORAL-DECOR-1 */
.about-spotlight { position:relative; isolation:isolate; }
.about-spotlight::before {
  content:""; position:absolute; z-index:0; pointer-events:none;
  top:0; left:0; width:min(29vw,310px); height:min(40vw,440px);
  background:url('/rose-and-co/assets/story-floral-spray.svg?v=story-decor1') left top / contain no-repeat;
  opacity:.48;
}
.about-spotlight::after {
  content:""; position:absolute; z-index:0; pointer-events:none;
  right:-1%; bottom:-10%; width:min(27vw,280px); height:min(33vw,380px);
  background:url('/rose-and-co/assets/story-floral-spray.svg?v=story-decor1') right bottom / contain no-repeat;
  transform:rotate(170deg); opacity:.30;
}
.about-spotlight .about-grid {position:relative;z-index:1;}
.spotlight-gallery .spotlight-large,
.spotlight-gallery .spotlight-small { border-color:#f7e9e5; }
.spotlight-gallery .spotlight-large {
  box-shadow:0 25px 62px rgba(96,46,61,.15);
}
.spotlight-gallery .spotlight-large img {
  object-fit:cover; object-position:center 48%; filter:saturate(.96) contrast(1.025);
}
.spotlight-gallery .spotlight-small {
  transform:rotate(2deg);
  box-shadow:0 18px 42px rgba(96,46,61,.15);
  border-radius:4px;
}
.spotlight-gallery .spotlight-small img {
  object-fit:cover; object-position:center 52%; filter:saturate(.91);
}
.about-stamp.about-stamp-rose.story-floral-seal {
  background:transparent; transform:rotate(-6deg);
  filter:drop-shadow(0 8px 13px rgba(100,46,64,.14));
}
.about-stamp.about-stamp-rose.story-floral-seal img {
  width:100%;height:100%;display:block;object-fit:contain;
}
.spotlight-copy {position:relative;z-index:1;}
@media (max-width:640px) {
  .about-spotlight::before {
    width:140px;height:204px;opacity:.22;
  }
  .about-spotlight::after {
    width:120px;height:170px;opacity:.19;
  }
  .spotlight-gallery .spotlight-small {transform:rotate(1.5deg);}
}
@media (prefers-reduced-motion:no-preference) and (hover:hover) {
  .story-floral-seal {transition:filter .5s ease, transform .65s cubic-bezier(.22,1,.36,1);}
  .spotlight-gallery:hover .story-floral-seal {
    transform:rotate(2deg) translateY(-3px);
    filter:drop-shadow(0 11px 17px rgba(100,46,64,.17));
  }
}
@media (prefers-reduced-motion:reduce) {
  .story-floral-seal {transition:none!important;}
}
'''
    css_path.write_text(css, encoding="utf-8")

# Bust old CSS cache without touching images elsewhere.
for page in root.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    text = re.sub(r'(/rose-and-co/assets/styles\.css)(?:\?v=[^"\']+)?',
                  r'\1?v=story-decor1', text)
    page.write_text(text, encoding="utf-8")
print(f"Rose & Co story decoration: {count} galleries, 2 florals, 1 botanical seal, no logo-wordmark changes.")
