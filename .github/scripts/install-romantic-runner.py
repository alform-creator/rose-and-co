#!/usr/bin/env python3
"""Rose & Co: subtle recurring 30-second bouquet delivery animation.

The animation is decorative, multilingual, accessible, lightweight, self-hosted,
responsive and dismissible. No original products, photos or SEO copy are changed.
Runs after all other page builders, including the story styling and opening intro.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
assets = root / "assets"
assert (root / "hy" / "index.html").is_file()

css = r'''
/* ROSE-CO-ROMANTIC-RUNNER-v1: illustrated gift of flowers every 30 seconds */
.rose-runner {
  position:fixed;
  left:50%;
  bottom:max(12px,env(safe-area-inset-bottom,0px));
  transform:translate(-50%,14px);
  width:min(435px,calc(100vw - 20px));
  height:189px;
  z-index:90;
  visibility:hidden;
  opacity:0;
  pointer-events:none;
  isolation:isolate;
  contain:layout paint;
}
.rose-runner.rose-runner-active {
  visibility:visible;
  animation:rr-scene-cycle 5.5s ease both;
}
.rose-runner-art {
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  filter:drop-shadow(0 8px 10px rgba(83,33,51,.12));
}
.rose-runner-close {
  appearance:none;
  position:absolute;
  top:19px;
  right:13px;
  z-index:4;
  display:grid;
  place-items:center;
  width:26px;
  height:26px;
  padding:0;
  border:1px solid rgba(111,46,67,.25);
  border-radius:100%;
  background:rgba(255,250,247,.94);
  color:#64273e;
  font:18px/1 system-ui,sans-serif;
  box-shadow:0 2px 8px rgba(70,34,47,.10);
  cursor:pointer;
  pointer-events:auto;
  -webkit-tap-highlight-color:transparent;
}
.rose-runner-close:hover,
.rose-runner-close:focus-visible {background:#64273e;color:#fff;}
.rose-runner-active .rr-boy {animation:rr-approach 4.5s cubic-bezier(.2,.65,.4,1) both;}
.rose-runner-active .rr-boy-body {animation:rr-bob .38s ease-in-out 7 alternate;}
.rose-runner-active .rr-left-leg {animation:rr-leg-left .32s ease-in-out 8 alternate;}
.rose-runner-active .rr-right-leg {animation:rr-leg-right .32s ease-in-out 8 alternate;}
.rose-runner-active .rr-bouquet {animation:rr-offer .7s 3.05s ease-out both;}
.rose-runner-active .rr-girl-hand {animation:rr-reach .8s 3.05s ease-out both;}
.rose-runner-active .rr-girl-head {animation:rr-girl-tilt 1s 3.05s ease-out both;}
.rose-runner-active .rr-heart {animation:rr-heart-pop 1.5s 3.3s ease-out both;}
.rose-runner-active .rr-heart.rr-h2 {animation-delay:3.55s;}
.rose-runner-active .rr-heart.rr-h3 {animation-delay:3.72s;}
.rose-runner-active .rr-spark {animation:rr-spark .95s 3.55s ease-out both;}
.rose-runner-active .rr-spark.rr-s2 {animation-delay:3.8s;}
@keyframes rr-scene-cycle {
  0% {opacity:0;transform:translate(-50%,20px)}
  7% {opacity:1;transform:translate(-50%,0)}
  86% {opacity:1;transform:translate(-50%,0)}
  100% {opacity:0;transform:translate(-50%,13px)}
}
@keyframes rr-approach {
  0% {transform:translateX(-126px)}
  10% {transform:translateX(-90px)}
  64% {transform:translateX(160px)}
  77%,100% {transform:translateX(174px)}
}
@keyframes rr-bob {0% {transform:translateY(0)} 100% {transform:translateY(-4px)}}
@keyframes rr-leg-left {0% {transform:rotate(17deg)} 100% {transform:rotate(-22deg)}}
@keyframes rr-leg-right {0% {transform:rotate(-24deg)} 100% {transform:rotate(19deg)}}
@keyframes rr-offer {
  0% {transform:translate(0,0) rotate(-5deg)}
  100% {transform:translate(13px,-6px) rotate(7deg)}
}
@keyframes rr-reach {
  0% {transform:rotate(0deg)}
  100% {transform:rotate(-19deg)}
}
@keyframes rr-girl-tilt {
  0% {transform:rotate(0deg)}
  100% {transform:rotate(-7deg)}
}
@keyframes rr-heart-pop {
  0% {opacity:0;transform:translateY(12px) scale(.45)}
  30% {opacity:1;transform:translateY(0) scale(1)}
  100% {opacity:0;transform:translateY(-26px) scale(1.13)}
}
@keyframes rr-spark {
  0%,100% {opacity:0;transform:scale(.5)}
  45% {opacity:1;transform:scale(1.1)}
}
.rr-left-leg,.rr-right-leg,.rr-girl-hand,.rr-girl-head {
  transform-box:fill-box;
}
.rr-left-leg,.rr-right-leg {transform-origin:top center;}
.rr-girl-hand {transform-origin:85% 85%;}
.rr-girl-head {transform-origin:50% 90%;}
.rr-heart,.rr-spark {opacity:0;transform-box:fill-box;transform-origin:center;}
.rose-runner:has(~ dialog[open]) {visibility:hidden !important;}
@media(max-width:640px) {
  .rose-runner {
    height:145px;
    bottom:max(10px,env(safe-area-inset-bottom,0px));
    width:min(335px,calc(100vw - 14px));
  }
  .rose-runner-close {top:7px;right:4px;width:25px;height:25px;}
}
@media(prefers-reduced-motion:reduce) {
  .rose-runner,.rose-runner.rose-runner-active {display:none !important;animation:none !important;}
}

/* ROSE-CO-ROMANTIC-RUNNER-SEE-IT-v2 */
/* Stage is obvious on mobile, yet stays beneath native modal dialogs. */
.rose-runner {
  width:min(485px,calc(100vw - 16px));
  height:211px;
  z-index:2147483000;
  bottom:max(8px,env(safe-area-inset-bottom,0px));
}
.rose-runner::before {
  content:"";
  position:absolute;
  z-index:-1;
  inset:26px 6px 4px;
  border-radius:115px 115px 34px 34px;
  background:
    radial-gradient(ellipse at 75% 23%,rgba(255,248,243,.91),transparent 64%),
    linear-gradient(140deg,rgba(255,249,246,.88),rgba(244,215,217,.93));
  box-shadow:0 8px 25px rgba(96,42,62,.12), inset 0 1px rgba(255,255,255,.8);
}
.rose-runner-art { z-index:1;filter:drop-shadow(0 5px 6px rgba(83,33,51,.13)); }
.rose-runner-close {top:24px;right:14px;z-index:6;}
@media(max-width:640px) {
  .rose-runner {
    width:min(390px,calc(100vw - 12px));
    height:177px;
    bottom:max(8px,env(safe-area-inset-bottom,0px));
  }
  .rose-runner::before {inset:16px 3px 2px;border-radius:90px 90px 22px 22px;}
  .rose-runner-close {top:12px;right:11px;}
}
/* Respect reduced-motion preference: show the illustrated exchange
   without motion, rather than making the entire feature disappear. */
@media (prefers-reduced-motion:reduce) {
  .rose-runner {display:block !important;}
  .rose-runner.rose-runner-active {
    visibility:visible;
    opacity:1;
    transform:translate(-50%,0);
    animation:none !important;
  }
  .rose-runner-active .rr-boy {transform:translateX(174px);}
  .rose-runner-active .rr-bouquet {transform:translate(13px,-6px) rotate(7deg);}
  .rose-runner-active .rr-girl-hand {transform:rotate(-19deg);}
  .rose-runner-active .rr-heart {
    opacity:.78;
    transform:translateY(0) scale(.8);
  }
  .rose-runner-active .rr-boy-body,
  .rose-runner-active .rr-left-leg,
  .rose-runner-active .rr-right-leg,
  .rose-runner-active .rr-girl-head,
  .rose-runner-active .rr-spark {animation:none !important;}
}
'''

# Detailed vector illustration, not emoji or floating text. The boy runs across
# a softly colored oval floor, offers a bouquet, and small hearts appear.
svg = r'''<svg class="rose-runner-art" viewBox="0 0 435 189" preserveAspectRatio="xMidYMax meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="rr-floor" x1="0" y1="0" x2="1" y2="0">
      <stop stop-color="#faebe6" stop-opacity="0"/>
      <stop offset=".25" stop-color="#f3d7d8" stop-opacity=".8"/>
      <stop offset=".75" stop-color="#f0d2d3" stop-opacity=".8"/>
      <stop offset="1" stop-color="#faebe6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rr-rose" x1="0" y1="0" x2=".85" y2="1">
      <stop stop-color="#ffe4df"/><stop offset=".54" stop-color="#eaaaaf"/><stop offset="1" stop-color="#ae536e"/>
    </linearGradient>
    <linearGradient id="rr-suit" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#82445b"/><stop offset="1" stop-color="#55263a"/>
    </linearGradient>
    <linearGradient id="rr-dress" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#f2c2c4"/><stop offset="1" stop-color="#bc758f"/>
    </linearGradient>
    <filter id="rr-blur"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <ellipse cx="218" cy="166" rx="204" ry="19" fill="#c58d9b" opacity=".12" filter="url(#rr-blur)"/>
  <path d="M18 167 Q208 162 418 167" fill="none" stroke="#bd9c9b" stroke-width="1" opacity=".45"/>
  <ellipse cx="218" cy="171" rx="205" ry="6" fill="url(#rr-floor)" opacity=".83"/>
  <g class="rr-girl">
    <ellipse cx="337" cy="165" rx="30" ry="5" fill="#75485b" opacity=".17"/>
    <!-- flowing hair behind the girl's face -->
    <path d="M319 61 Q317 40 329 35 Q347 29 355 46 Q360 56 355 72 Q363 83 357 97 Q346 104 333 95 Q313 98 312 86 Q317 73 319 61Z" fill="#563c36"/>
    <path d="M326 88 Q336 94 347 87 L351 106 L323 107Z" fill="#e7b89c"/>
    <!-- sweeping dress -->
    <path d="M327 97 Q341 91 352 100 Q350 120 362 160 Q343 168 309 160 Q324 119 327 97Z" fill="url(#rr-dress)"/>
    <path d="M331 103 Q335 121 320 157 M350 108 Q351 133 357 154" fill="none" stroke="#fff1ec" stroke-width="2.5" opacity=".52"/>
    <path d="M313 160 Q337 166 362 160" fill="none" stroke="#a35f7b" stroke-width="3"/>
    <path d="M325 160 L324 168 M349 161 L351 168" stroke="#a57967" stroke-width="5" stroke-linecap="round"/>
    <!-- graceful shoulder / bouquet-reaching arm -->
    <path d="M324 105 Q316 116 322 129" fill="none" stroke="#e5b79c" stroke-width="7" stroke-linecap="round"/>
    <g class="rr-girl-hand">
      <path d="M350 108 Q332 107 316 112 Q307 116 303 119" fill="none" stroke="#e5b79c" stroke-width="7" stroke-linecap="round"/>
      <circle cx="302" cy="120" r="4" fill="#e5b79c"/>
    </g>
    <g class="rr-girl-head">
      <ellipse cx="336" cy="61" rx="17" ry="21" fill="#edbfa2"/>
      <path d="M319 57 Q317 40 329 37 Q342 33 352 44 Q347 48 340 47 Q335 57 321 59Z" fill="#62423a"/>
      <path d="M350 53 Q358 72 352 91" fill="none" stroke="#62423a" stroke-width="8" stroke-linecap="round"/>
      <circle cx="330" cy="64" r="1.6" fill="#5e3b38"/>
      <circle cx="342" cy="64" r="1.6" fill="#5e3b38"/>
      <path d="M331 73 Q337 78 343 72" fill="none" stroke="#b16e6f" stroke-width="1.8" stroke-linecap="round"/>
      <circle cx="326" cy="70" r="3" fill="#e7a0a1" opacity=".48"/>
    </g>
  </g>
  <g class="rr-boy">
    <ellipse cx="88" cy="165" rx="27" ry="5" fill="#75485b" opacity=".16"/>
    <g class="rr-boy-body">
      <!-- arms and trousers are layered behind the jacket -->
      <g class="rr-left-leg">
        <path d="M79 124 Q71 141 68 160" fill="none" stroke="#524854" stroke-width="9" stroke-linecap="round"/>
        <path d="M68 160 Q60 166 52 165" fill="none" stroke="#352e3c" stroke-width="6" stroke-linecap="round"/>
      </g>
      <g class="rr-right-leg">
        <path d="M95 124 Q99 143 109 159" fill="none" stroke="#625061" stroke-width="9" stroke-linecap="round"/>
        <path d="M109 159 L123 162" fill="none" stroke="#3b3240" stroke-width="6" stroke-linecap="round"/>
      </g>
      <!-- suit and collar -->
      <path d="M82 86 Q92 82 103 91 L107 129 Q94 135 77 126Z" fill="url(#rr-suit)"/>
      <path d="M92 86 L95 109 L101 91" fill="#f9f1e8"/>
      <path d="M96 98 L94 110" stroke="#ad7891" stroke-width="2"/>
      <path d="M84 91 Q74 108 83 120" fill="none" stroke="#70374c" stroke-width="9" stroke-linecap="round"/>
      <circle cx="84" cy="120" r="4" fill="#eab99e"/>
      <!-- face and short hair -->
      <path d="M88 80 L92 92 L101 91 L103 78" fill="#e5b598"/>
      <ellipse cx="94" cy="63" rx="17" ry="20" fill="#eac0a2"/>
      <path d="M77 61 Q75 42 90 39 Q108 34 112 51 L110 57 Q104 52 99 47 Q92 56 81 54Z" fill="#3d3035"/>
      <path d="M77 62 Q73 51 81 47" fill="none" stroke="#3d3035" stroke-width="5" stroke-linecap="round"/>
      <circle cx="99" cy="65" r="1.5" fill="#593b3e"/>
      <path d="M99 74 Q103 77 107 72" fill="none" stroke="#a56a69" stroke-width="1.7" stroke-linecap="round"/>
      <!-- the offered arm follows the running body -->
      <path d="M104 96 Q115 104 126 111" fill="none" stroke="#6c344d" stroke-width="10" stroke-linecap="round"/>
      <circle cx="126" cy="111" r="4.9" fill="#e8ba9a"/>
      <g class="rr-bouquet">
        <!-- green foliage and stems -->
        <path d="M129 111 L140 83 M131 111 L130 79 M128 110 L116 87 M131 111 L150 96" stroke="#638069" stroke-width="3" stroke-linecap="round"/>
        <path d="M135 100 Q117 97 117 81 Q136 83 135 100Z M134 98 Q149 80 157 84 Q150 100 134 98Z M129 100 Q105 96 109 88 Q124 86 129 100Z" fill="#78967e"/>
        <path d="M122 105 L136 116 L144 102" fill="#f8e2d7" stroke="#d8a7a0" stroke-width="1.5"/>
        <path d="M115 94 L142 117 L156 95" fill="#eecbd0" opacity=".72"/>
        <path d="M125 110 L138 114" fill="none" stroke="#b68195" stroke-width="2"/>
        <!-- flower blooms -->
        <g fill="url(#rr-rose)" stroke="#a45b76" stroke-width=".65">
          <circle cx="129" cy="77" r="11"/>
          <circle cx="115" cy="85" r="9"/>
          <circle cx="145" cy="84" r="10"/>
          <circle cx="152" cy="96" r="8"/>
        </g>
        <g fill="none" stroke="#fdf0e9" stroke-width="2" stroke-linecap="round">
          <path d="M125 75 Q130 70 134 77 Q130 84 126 79"/>
          <path d="M112 84 Q115 80 120 86"/>
          <path d="M141 83 Q144 78 149 84"/>
          <path d="M148 95 Q152 92 155 97"/>
        </g>
        <path d="M127 109 Q130 105 134 109" stroke="#ad7186" stroke-width="2" fill="none"/>
      </g>
    </g>
  </g>
  <!-- celebrating the exchange -->
  <g class="rr-heart" fill="#ba647e">
    <path d="M289 56 C278 45 281 35 290 35 Q297 35 300 42 Q304 34 311 35 Q322 40 313 51 L300 64Z"/>
  </g>
  <g class="rr-heart rr-h2" fill="#db93a7">
    <path d="M311 27 C306 20 308 15 314 15 Q319 15 321 19 Q326 12 331 16 Q337 22 330 29 L321 38Z"/>
  </g>
  <g class="rr-heart rr-h3" fill="#d8aa9b">
    <path d="M268 30 C264 25 266 20 270 20 Q274 20 276 24 Q280 19 284 22 Q289 27 283 32 L276 38Z"/>
  </g>
  <g class="rr-spark" fill="none" stroke="#c59b78" stroke-width="2" stroke-linecap="round">
    <path d="M293 77 v-7 m-4 4 h8"/>
  </g>
  <g class="rr-spark rr-s2" fill="none" stroke="#bc8396" stroke-width="2" stroke-linecap="round">
    <path d="M317 78 v-7 m-4 4 h8"/>
  </g>
</svg>'''

# Keep all elements under one component and only show it when JS deliberately
# adds the "active" class. Avoid modifying any existing product/modal markup.
markup = r'''<div class="rose-runner" id="rose-runner" data-cycle-ms="30000">
  <button type="button" class="rose-runner-close" aria-label="__CLOSE__" title="__CLOSE__">×</button>
  __SVG__
</div>'''
js = r'''(() => {
  "use strict";
  const stage = document.getElementById("rose-runner");
  if (!stage) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const intervalMs = 30000;  // Every thirty seconds after the first preview
  const durationMs = 6500;
  const closeButton = stage.querySelector(".rose-runner-close");
  let dismissed = reduced.matches;
  try { dismissed = dismissed || sessionStorage.getItem('rose-runner-dismissed') === '1'; } catch {}
  let finishTimer = null;
  let intervalTimer = null;
  let startTimer = null;

  function clearScene() {
    if (finishTimer !== null) {
      window.clearTimeout(finishTimer);
      finishTimer = null;
    }
    stage.classList.remove("rose-runner-active");
  }

  function canPlay() {
    return !dismissed && !document.hidden &&
      !document.documentElement.classList.contains("rose-bloom-on") &&
      !document.querySelector("dialog[open], [aria-modal='true']");
  }

  function play() {
    if (!canPlay()) return;
    clearScene();
    // Force keyframes to restart on every 30s appearance, also on iOS Safari.
    void stage.offsetWidth;
    stage.classList.add("rose-runner-active");
    finishTimer = window.setTimeout(clearScene, durationMs);
  }

  function begin() {
    if (dismissed || intervalTimer !== null || startTimer !== null) return;
    // On homepages, do not cover the separate flower-growing intro.
    // On interior pages, the first gift appears almost immediately.
    const delay = 30000;
    startTimer = window.setTimeout(() => {
      startTimer = null;
      play();
      intervalTimer = window.setInterval(play, intervalMs);
    }, delay);
  }

  function stopTimers() {
    if (startTimer !== null) window.clearTimeout(startTimer);
    if (intervalTimer !== null) window.clearInterval(intervalTimer);
    startTimer = null;
    intervalTimer = null;
    clearScene();
  }

  closeButton?.addEventListener("click", () => {
    dismissed = true;
    try { sessionStorage.setItem('rose-runner-dismissed', '1'); } catch {}
    stopTimers();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) clearScene();
  });
  window.addEventListener("pagehide", stopTimers);
  window.addEventListener("pageshow", () => {
    if (!dismissed) begin();
  });
  begin();
})();'''

(assets / "romantic-runner.css").write_text(css + "\n", encoding="utf-8")
(assets / "romantic-runner.js").write_text(js + "\n", encoding="utf-8")

locales = {
    "hy": "Փակել ծաղիկներ նվիրելու անիմացիան",
    "ru": "Закрыть анимацию с цветами",
    "en": "Dismiss flower delivery animation",
}
total = 0
for lang, close_label in locales.items():
    pages = list((root / lang).rglob("*.html"))
    assert pages, f"Missing pages for {lang}"
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert 'id="rose-runner"' not in html, f"Unexpected duplicate in {page}"
        assert "</head>" in html and "</body>" in html, f"Unexpected page: {page}"
        art = markup.replace("__CLOSE__", close_label).replace("__SVG__", svg)
        html = html.replace("</head>",
            '<link rel="stylesheet" href="/rose-and-co/assets/romantic-runner.css?v=runner2"/>' +
            '<script defer src="/rose-and-co/assets/romantic-runner.js?v=runner2"></script>' +
            "</head>", 1)
        html = html.replace("</body>", art + "</body>", 1)
        page.write_text(html, encoding="utf-8")
        total += 1

assert total >= 18, f"Expected complete locale coverage, got {total}"
assert sum('id="rose-runner"' in p.read_text(encoding="utf-8")
           for p in root.glob("*/index.html")) == 3
print(f"Rose & Co romantic bouquet runner installed on {total} pages across HY/RU/EN, 30-second cycle.")
