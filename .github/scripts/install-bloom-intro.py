#!/usr/bin/env python3
"""Add Rose & Co's elegant, accessible 'flower growing from earth' site entrance.

Only the HY/RU/EN homepages receive the intro. The original hero image, all
catalog products, copy, SEO headings, and navigation stay unchanged.
"""
from pathlib import Path
import sys
import base64

root = Path(sys.argv[1]).resolve()
assets = root / "assets"
assert (root / "hy" / "index.html").exists()

css = r'''
/* Rose & Co — botanical entrance, independent from the original hero image. */
.rose-bloom-overlay { display: none; }
html.rose-bloom-on .rose-bloom-overlay {
  position: fixed; inset: 0; z-index: 9999; display: flex;
  flex-direction: column; align-items: center; justify-content: center;
  min-height: 100vh; min-height: 100dvh; width: 100%;
  padding: max(30px,env(safe-area-inset-top)) 24px max(28px,env(safe-area-inset-bottom));
  overflow: hidden; isolation: isolate; text-align: center; color: #632f42;
  background: radial-gradient(ellipse at 50% 40%, #fffaf5 0%, #f9eee9 46%, #eacfd0 100%);
  animation: rb-leave .65s 3.8s forwards;
}
.rose-bloom-overlay::before,
.rose-bloom-overlay::after {
  position: absolute; content: ""; border-radius: 50%; pointer-events: none; z-index: -1;
}
.rose-bloom-overlay::before {
  height: min(70vw,550px); width: min(70vw,550px);
  top: 10%; left: -15%; border: 1px solid rgba(166,102,114,.13);
}
.rose-bloom-overlay::after {
  width: min(52vw,370px); height: min(52vw,370px);
  bottom: -18%; right: -10%; border: 1px solid rgba(166,102,114,.13);
}
.rose-bloom-brand {
  position: absolute; top: max(45px,env(safe-area-inset-top)); left: 0; right: 0;
  font-family: Georgia, serif; font-size: clamp(16px, 3vw, 21px);
  font-weight: normal; letter-spacing: .24em; color: #713247;
  opacity: 0; animation: rb-caption-in .85s .13s forwards;
}
.rose-bloom-brand span { color: #b78f93; font-style: italic; }
.rose-bloom-skip {
  position: absolute; right: max(24px,env(safe-area-inset-right));
  top: max(32px,env(safe-area-inset-top));
  color: #793f53; border: 1px solid rgba(120,61,82,.24);
  background: rgba(255,255,255,.53); border-radius: 40px;
  padding: 9px 17px; font: 500 12px/1.3 'DM Sans','Noto Sans Armenian',sans-serif;
  letter-spacing: .015em; cursor: pointer; z-index: 2;
  transition: color .2s, background .2s, border-color .2s;
}
.rose-bloom-skip:hover,
.rose-bloom-skip:focus-visible {
  color: #fff; background: #6e3048; border-color: #6e3048;
}
.rose-bloom-scene {
  position: relative; width: min(420px,83vw,47vh); min-width: min(290px,83vw);
  aspect-ratio: 420/390; margin: 12px 0 6px; flex: 0 1 auto;
}
.rose-bloom-scene::before {
  position: absolute; inset: 16% 0 3%; content: ""; border-radius: 50%;
  background: radial-gradient(circle at center,rgba(255,255,255,.66),rgba(255,255,255,0) 66%);
}
.rose-bloom-svg { display: block; width: 100%; height: 100%; overflow: visible; position: relative; }
.rb-soil { opacity: 0; animation: rb-soil-in 1s .1s forwards; }
.rb-stem {
  fill: none; stroke: #526e58; stroke-width: 7.7; stroke-linecap: round;
  stroke-dasharray: 250; stroke-dashoffset: 250;
  animation: rb-stem-grow 1.75s .48s cubic-bezier(.28,.05,.16,1) forwards;
}
.rb-leaf-left, .rb-leaf-right {
  opacity: 0; transform-box: fill-box;
  transform: rotate(-30deg) scale(.08);
  animation: rb-leaf-open .72s cubic-bezier(.17,.82,.3,1.18) forwards;
}
.rb-leaf-left { transform-origin: 96% 92%; animation-delay: 1.08s; }
.rb-leaf-right { transform-origin: 5% 94%; animation-delay: 1.48s; }
.rb-leaf-right { transform: rotate(35deg) scale(.08); }
.rb-bud {
  opacity: 0; transform-origin: center bottom; transform-box: fill-box;
  animation: rb-bud-rise 1.05s 1.56s both;
}
.rb-petals {
  opacity: 0; transform-origin: center; transform-box: fill-box;
  transform: scale(.15) rotate(-35deg);
  animation: rb-flower-open 1.15s 2.02s cubic-bezier(.18,.65,.16,1) forwards;
}
.rb-flower-core {
  opacity: 0; animation: rb-core-in .65s 2.60s both;
}
.rb-sparkle { opacity: 0; animation: rb-sparkle-pop .8s 2.62s both; }
.rb-sparkle:nth-child(2) { animation-delay:2.75s; }
.rb-sparkle:nth-child(3) { animation-delay:2.85s; }
.rose-bloom-caption {
  font: 400 clamp(18px,3.9vw,25px)/1.45 'Playfair Display',Georgia,'Noto Sans Armenian',serif;
  letter-spacing: -.015em; margin: 4px 0 0;
  color: #763c51; opacity: 0; transform: translateY(8px);
  animation: rb-caption-in .78s 2.28s forwards;
}
.rose-bloom-subtitle {
  margin: 11px 0 0; font: 600 10px/1.3 'DM Sans',sans-serif;
  letter-spacing: .34em; color: #a88288; opacity: 0;
  animation: rb-caption-in .8s 2.45s forwards;
}
html.rose-bloom-on .rose-bloom-overlay.rose-bloom-closing {
  animation: rb-leave .48s 0s forwards;
}
@keyframes rb-soil-in { from {opacity:0;transform:translateY(8px)} to {opacity:1;transform:translateY(0)} }
@keyframes rb-stem-grow { to {stroke-dashoffset:0} }
@keyframes rb-leaf-open { to {opacity:1;transform:rotate(0deg) scale(1)} }
@keyframes rb-bud-rise {
  0%,10% {opacity:0;transform:scale(.1)}
  48% {opacity:1;transform:scale(1)}
  80% {opacity:1;transform:scale(1)}
  100% {opacity:0;transform:scale(1.12)}
}
@keyframes rb-flower-open {
  0% {opacity:0;transform:scale(.15) rotate(-35deg)}
  26% {opacity:1}
  75% {transform:scale(1.06) rotate(3deg)}
  100% {opacity:1;transform:scale(1) rotate(0deg)}
}
@keyframes rb-core-in { from {opacity:0;transform:scale(.2)} to {opacity:1;transform:scale(1)} }
@keyframes rb-sparkle-pop {
  0% {opacity:0;transform:translateY(5px) scale(.4)}
  40% {opacity:.88;transform:translateY(-4px) scale(1)}
  100% {opacity:0;transform:translateY(-13px) scale(.5)}
}
@keyframes rb-caption-in {to {opacity:1;transform:translateY(0)}}
@keyframes rb-leave {
  0% {opacity:1;visibility:visible}
  100% {opacity:0;visibility:hidden;pointer-events:none}
}
@media(max-width:640px) {
  .rose-bloom-brand { top:max(63px,env(safe-area-inset-top)); font-size:17px; }
  .rose-bloom-skip { top:max(20px,env(safe-area-inset-top));right:17px;font-size:11px;padding:8px 13px; }
  .rose-bloom-scene { width:min(355px,85vw,47vh);min-width:0; }
  .rose-bloom-caption { font-size:clamp(17px,5vw,23px); }
}
@media (prefers-reduced-motion: reduce) {
  .rose-bloom-overlay { display:none !important; }
}
'''

css += '\n' + (Path(__file__).resolve().parent/'bloom-luxury.css').read_text(encoding='utf-8')

js = r'''(() => {
  "use strict";
  const root = document.documentElement;
  const overlay = document.querySelector(".rose-bloom-overlay");
  if (!overlay || !root.classList.contains("rose-bloom-on")) return;
  const skip = overlay.querySelector(".rose-bloom-skip");
  let closed = false;
  let cleanupTimer = null;
  function closeBloom() {
    if (closed) return;
    closed = true;
    overlay.classList.add("rose-bloom-closing");
    if (cleanupTimer) clearTimeout(cleanupTimer);
    cleanupTimer = setTimeout(() => {
      root.classList.remove("rose-bloom-on");
      overlay.remove();
    }, 520);
  }
  skip?.addEventListener("click", closeBloom);
  const onKey = (e) => { if (e.key === "Escape") closeBloom(); };
  document.addEventListener("keydown", onKey);
  const timer = setTimeout(closeBloom, 5900);
  window.addEventListener("pagehide", () => {
    clearTimeout(timer);
    document.removeEventListener("keydown", onKey);
  }, { once: true });
  // Do not keep the overlay hanging if the tab becomes hidden.
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) closeBloom();
  });
})();'''

head_gate = r'''<script id="rose-bloom-gate">
(function(){
  try {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var force = new URL(window.location.href).searchParams.get("intro") === "1";
    var played = window.sessionStorage.getItem("roseBloomPlayed");
    if (!played || force) {
      document.documentElement.classList.add("rose-bloom-on");
      window.sessionStorage.setItem("roseBloomPlayed", "1");
    }
  } catch(e) {
    document.documentElement.classList.add("rose-bloom-on");
  }
})();
</script>'''

# The original homepage hero is NOT changed: this decorative SVG sits above the
# page briefly and is removed, once, after the entrance completes.
markup = r'''<div class="rose-bloom-overlay" role="region" aria-label="__ARIA__">
  <div class="rose-bloom-brand" aria-hidden="true">ROSE <span>&amp;</span> CO<small>FLORAL ATELIER · ARMENIA</small></div>
  <button class="rose-bloom-skip" type="button">__SKIP__ <span aria-hidden="true">↗</span></button>
  <div class="rose-bloom-scene" aria-hidden="true">
    <svg class="rose-bloom-svg" viewBox="0 0 420 390" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="rb-ground" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#a27b68"/><stop offset="1" stop-color="#705447"/></linearGradient>
        <linearGradient id="rb-leafshade" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#80a38a"/><stop offset="1" stop-color="#3d654e"/></linearGradient>
        <linearGradient id="rb-pink" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff0e5"/><stop offset=".56" stop-color="#e2a9b5"/><stop offset="1" stop-color="#b96d87"/></linearGradient>
        <radialGradient id="rb-center" cx=".42" cy=".35" r=".8"><stop stop-color="#ffe5bf"/><stop offset=".65" stop-color="#dba985"/><stop offset="1" stop-color="#a96971"/></radialGradient>
        <filter id="rb-shadow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>
      </defs>
      <g class="rb-soil">
        <ellipse cx="209" cy="332" rx="115" ry="13" fill="#6e5253" opacity=".17" filter="url(#rb-shadow)"/>
        <path d="M105 327 C145 321 172 315 210 316 C256 316 279 323 316 327 C292 338 135 337 105 327Z" fill="url(#rb-ground)"/>
        <path d="M140 325 C165 320 186 318 209 318 C244 317 273 322 288 326" fill="none" stroke="#c5a38c" stroke-width="2" stroke-linecap="round" opacity=".8"/>
        <circle cx="153" cy="337" r="2.6" fill="#aa7f72"/><circle cx="264" cy="337" r="2" fill="#b58a77"/>
        <circle cx="305" cy="330" r="2" fill="#a58172"/><circle cx="117" cy="331" r="1.7" fill="#be9d8b"/>
      </g>
      <path class="rb-stem" d="M210 319 C211 289 205 268 208 240 S205 200 210 170 S213 156 210 152"/>
      <path class="rb-leaf-left" d="M210 265 C193 236 170 224 140 226 C154 251 169 265 210 265Z" fill="url(#rb-leafshade)"/>
      <path class="rb-leaf-left" d="M210 265 Q174 245 151 232" fill="none" stroke="#b9d3b6" stroke-width="2" opacity=".5"/>
      <path class="rb-leaf-right" d="M207 226 C224 201 247 191 272 197 C264 223 240 234 207 226Z" fill="url(#rb-leafshade)"/>
      <path class="rb-leaf-right" d="M207 226 Q242 213 259 202" fill="none" stroke="#b9d3b6" stroke-width="2" opacity=".5"/>
      <g transform="translate(210 151)">
        <ellipse class="rb-bud" cx="0" cy="-6" rx="11" ry="17" fill="#c9778d"/>
        <g class="rb-petals" fill="url(#rb-pink)">
          <path d="M0 31 C-34 38 -68 4 -57 -23 C-52 -40 -35 -43 -21 -39 C-15 -62 20 -67 34 -43 C55 -49 74 -27 59 -7 C66 14 36 42 0 31Z"/>
          <path d="M-2 29 C-35 24 -53 -5 -38 -26 C-25 -44 -2 -38 10 -20 C37 -47 61 -24 45 -3 C34 15 16 29 -2 29Z" fill="#f1c7ca"/>
          <path d="M-29 -21 C-24 -49 9 -54 22 -33 C34 -20 26 0 9 10 C-8 9 -31 -1 -29 -21Z" fill="#f8e0dc"/>
          <path d="M-25 3 C-41 -15 -22 -31 -5 -20 C9 -41 34 -28 27 -9 C25 7 4 25 -11 17Z" fill="#e9b5bf"/>
          <path d="M-11 -15 C-2 -29 23 -15 13 -2 C6 9 -10 7 -11 -4 C-10 -11 2 -13 4 -5" fill="#f8ddd8"/>
          <path d="M-51 -17 C-42 -3 -39 16 -15 24 M33 -35 C36 -18 47 -15 44 0 M-21 -39 C-9 -35 -2 -29 0 -19" fill="none" stroke="#c18b96" stroke-width="1" opacity=".65"/>
        </g>
        <g class="rb-flower-core">
          <circle cx="0" cy="0" r="7" fill="#e4b0ba" opacity=".7"/>
          <path d="M-9 -2 C-3 -12 11 -9 10 1 C9 12 -6 12 -8 3 C-9 -1 -1 -5 3 0" fill="none" stroke="#b87589" stroke-width="1.2" stroke-linecap="round" opacity=".82"/>
        </g>
      </g>
      <g fill="#c59e93">
        <circle class="rb-sparkle" cx="140" cy="106" r="3"/>
        <circle class="rb-sparkle" cx="280" cy="112" r="2.4"/>
        <circle class="rb-sparkle" cx="259" cy="72" r="2.3"/>
      </g>
    </svg>
  </div>
  <p class="rose-bloom-caption" aria-label="__CAPTION__"><span>__LEAD__</span><span class="rb-caption-middle">__MIDDLE__</span><span class="rb-caption-accent">__ACCENT__</span></p>
  <span class="rose-bloom-subtitle" aria-hidden="true">FLOWERS WITH FEELING</span>
</div>'''

translations = {
 "hy": {"lead":"Գեղեցկությունը","middle":"ծաղկում է","accent":"նրբորեն","skip":"Բաց թողնել","caption":"Գեղեցկությունը ծաղկում է նրբորեն","aria":"Ծաղկի աճելու ներածական անիմացիա"},
 "ru": {"lead":"Красота","middle":"расцветает","accent":"нежно","skip":"Пропустить","caption":"Красота расцветает нежно","aria":"Вступительная анимация: растёт цветок"},
 "en": {"lead":"Beauty","middle":"blooms","accent":"gently","skip":"Skip intro","caption":"Beauty blooms gently","aria":"Opening animation of a growing flower"},
}
(assets / "bloom-intro.css").write_text(css + "\n", encoding="utf-8")
(assets / "bloom-intro.js").write_text(js + "\n", encoding="utf-8")

# Locally served Armenian display type: available during the opening scene.
fontdir=assets/'fonts'
fontdir.mkdir(exist_ok=True)
(fontdir/'NotoSerifArmenian-SemiCondensedLight.woff').write_bytes(base64.b64decode("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"))
(fontdir/'Noto-Armenian-OFL.txt').write_text('Copyright 2022 The Noto Project Authors (https://github.com/notofonts/armenian)\n\nThis Font Software is licensed under the SIL Open Font License, Version 1.1.\nThis license is copied below, and is also available with a FAQ at:\nhttps://scripts.sil.org/OFL\n\n\n-----------------------------------------------------------\nSIL OPEN FONT LICENSE Version 1.1 - 26 February 2007\n-----------------------------------------------------------\n\nPREAMBLE\nThe goals of the Open Font License (OFL) are to stimulate worldwide\ndevelopment of collaborative font projects, to support the font creation\nefforts of academic and linguistic communities, and to provide a free and\nopen framework in which fonts may be shared and improved in partnership\nwith others.\n\nThe OFL allows the licensed fonts to be used, studied, modified and\nredistributed freely as long as they are not sold by themselves. The\nfonts, including any derivative works, can be bundled, embedded, \nredistributed and/or sold with any software provided that any reserved\nnames are not used by derivative works. The fonts and derivatives,\nhowever, cannot be released under any other type of license. The\nrequirement for fonts to remain under this license does not apply\nto any document created using the fonts or their derivatives.\n\nDEFINITIONS\n"Font Software" refers to the set of files released by the Copyright\nHolder(s) under this license and clearly marked as such. This may\ninclude source files, build scripts and documentation.\n\n"Reserved Font Name" refers to any names specified as such after the\ncopyright statement(s).\n\n"Original Version" refers to the collection of Font Software components as\ndistributed by the Copyright Holder(s).\n\n"Modified Version" refers to any derivative made by adding to, deleting,\nor substituting -- in part or in whole -- any of the components of the\nOriginal Version, by changing formats or by porting the Font Software to a\nnew environment.\n\n"Author" refers to any designer, engineer, programmer, technical\nwriter or other person who contributed to the Font Software.\n\nPERMISSION & CONDITIONS\nPermission is hereby granted, free of charge, to any person obtaining\na copy of the Font Software, to use, study, copy, merge, embed, modify,\nredistribute, and sell modified and unmodified copies of the Font\nSoftware, subject to the following conditions:\n\n1) Neither the Font Software nor any of its individual components,\nin Original or Modified Versions, may be sold by itself.\n\n2) Original or Modified Versions of the Font Software may be bundled,\nredistributed and/or sold with any software, provided that each copy\ncontains the above copyright notice and this license. These can be\nincluded either as stand-alone text files, human-readable headers or\nin the appropriate machine-readable metadata fields within text or\nbinary files as long as those fields can be easily viewed by the user.\n\n3) No Modified Version of the Font Software may use the Reserved Font\nName(s) unless explicit written permission is granted by the corresponding\nCopyright Holder. This restriction only applies to the primary font name as\npresented to the users.\n\n4) The name(s) of the Copyright Holder(s) or the Author(s) of the Font\nSoftware shall not be used to promote, endorse or advertise any\nModified Version, except to acknowledge the contribution(s) of the\nCopyright Holder(s) and the Author(s) or with their explicit written\npermission.\n\n5) The Font Software, modified or unmodified, in part or in whole,\nmust be distributed entirely under this license, and must not be\ndistributed under any other license. The requirement for fonts to\nremain under this license does not apply to any document created\nusing the Font Software.\n\nTERMINATION\nThis license becomes null and void if any of the above conditions are\nnot met.\n\nDISCLAIMER\nTHE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT\nOF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL THE\nCOPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,\nINCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL\nDAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM\nOTHER DEALINGS IN THE FONT SOFTWARE.\n',encoding='utf-8')

count = 0
for lang, words in translations.items():
    page = root / lang / "index.html"
    text = page.read_text(encoding="utf-8")
    if "rose-bloom-overlay" in text:
        raise RuntimeError("Intro already installed; use a clean build: " + str(page))
    if "<head>" not in text or "<body>" not in text:
        raise RuntimeError("Expected home page structure: " + str(page))
    intro = (markup.replace("__SKIP__", words["skip"])
                   .replace("__CAPTION__", words["caption"])
                   .replace("__ARIA__", words["aria"])
                   .replace("__LEAD__", words["lead"])
                   .replace("__MIDDLE__", words["middle"])
                   .replace("__ACCENT__", words["accent"]))
    text = text.replace("<head>", "<head>" + head_gate, 1)
    text = text.replace("</head>",
        '<link rel="preload" href="/rose-and-co/assets/fonts/NotoSerifArmenian-SemiCondensedLight.woff" as="font" type="font/woff" crossorigin="anonymous"/>'
        '<link rel="stylesheet" href="/rose-and-co/assets/bloom-intro.css?v=luxury3"/>'
        '<script defer src="/rose-and-co/assets/bloom-intro.js?v=luxury3"></script>'
        '</head>', 1)
    text = text.replace("<body>", "<body>" + intro, 1)
    page.write_text(text, encoding="utf-8")
    count += 1
assert count == 3
print("Rose & Co animated bloom entrance installed on 3 language homepages; hero unchanged.")
