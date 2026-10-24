#!/usr/bin/env python3
"""Add Rose & Co's elegant, accessible 'flower growing from earth' site entrance.

Only the HY/RU/EN homepages receive the intro. The original hero image, all
catalog products, copy, SEO headings, and navigation stay unchanged.
"""
from pathlib import Path
import sys

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
  const timer = setTimeout(closeBloom, 3930);
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
  <div class="rose-bloom-brand" aria-hidden="true">ROSE <span>&amp;</span> CO</div>
  <button class="rose-bloom-skip" type="button">__SKIP__ <span aria-hidden="true">↗</span></button>
  <div class="rose-bloom-scene" aria-hidden="true">
    <svg class="rose-bloom-svg" viewBox="0 0 420 390" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="rb-ground" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#a27b68"/><stop offset="1" stop-color="#705447"/></linearGradient>
        <linearGradient id="rb-leafshade" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#80a38a"/><stop offset="1" stop-color="#3d654e"/></linearGradient>
        <linearGradient id="rb-pink" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f9d9db"/><stop offset=".56" stop-color="#dd91a7"/><stop offset="1" stop-color="#b85e83"/></linearGradient>
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
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(0)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(45)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(90)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(135)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(180)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(225)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(270)"/>
          <ellipse cx="0" cy="-30" rx="19" ry="33" transform="rotate(315)"/>
        </g>
        <g class="rb-flower-core">
          <circle cx="0" cy="0" r="19" fill="url(#rb-center)"/>
          <path d="M-9 -2 C-3 -12 11 -9 10 1 C9 12 -6 12 -8 3 C-9 -1 -1 -5 3 0" fill="none" stroke="#b77770" stroke-width="2.1" stroke-linecap="round" opacity=".82"/>
        </g>
      </g>
      <g fill="#c59e93">
        <circle class="rb-sparkle" cx="140" cy="106" r="3"/>
        <circle class="rb-sparkle" cx="280" cy="112" r="2.4"/>
        <circle class="rb-sparkle" cx="259" cy="72" r="2.3"/>
      </g>
    </svg>
  </div>
  <p class="rose-bloom-caption">__CAPTION__</p>
  <span class="rose-bloom-subtitle" aria-hidden="true">FLOWERS WITH FEELING</span>
</div>'''

translations = {
 "hy": {"skip":"Բաց թողնել","caption":"Գեղեցկությունը ծաղկում է նրբորեն","aria":"Ծաղկի աճելու ներածական անիմացիա"},
 "ru": {"skip":"Пропустить","caption":"Красота расцветает нежно","aria":"Вступительная анимация: растёт цветок"},
 "en": {"skip":"Skip intro","caption":"Beauty blooms gently","aria":"Opening animation of a growing flower"},
}
(assets / "bloom-intro.css").write_text(css + "\n", encoding="utf-8")
(assets / "bloom-intro.js").write_text(js + "\n", encoding="utf-8")
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
                   .replace("__ARIA__", words["aria"]))
    text = text.replace("<head>", "<head>" + head_gate, 1)
    text = text.replace("</head>",
        '<link rel="stylesheet" href="/rose-and-co/assets/bloom-intro.css?v=bloom1"/>'
        '<script defer src="/rose-and-co/assets/bloom-intro.js?v=bloom1"></script>'
        '</head>', 1)
    text = text.replace("<body>", "<body>" + intro, 1)
    page.write_text(text, encoding="utf-8")
    count += 1
assert count == 3
print("Rose & Co animated bloom entrance installed on 3 language homepages; hero unchanged.")
