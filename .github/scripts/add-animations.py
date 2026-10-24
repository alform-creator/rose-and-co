#!/usr/bin/env python3
"""Install light, accessible editorial motion across all Rose & Co pages.

Run after install-real-photos.py when the unpacked website is complete.
No external animation libraries, source-photo edits, or layout changes.
"""
from pathlib import Path
import sys
import re

root = Path(sys.argv[1]).resolve()
css_path = root / "assets" / "styles.css"
js_path = root / "assets" / "rose-motion.js"
css_marker = "/* ROSE-CO-PREMIUM-MOTION-v1 */"

css = r'''
/* ROSE-CO-PREMIUM-MOTION-v1 */
/* Editorial movement, respectful of accessibility and mobile performance. */
:root { --rose-ease: cubic-bezier(.22, 1, .36, 1); }
@media (prefers-reduced-motion: no-preference) {
  html.rose-motion-on [data-rose-reveal] {
    transition: opacity .76s var(--rose-ease),
                transform .86s var(--rose-ease);
    transition-delay: var(--rose-delay, 0ms);
  }
  html.rose-motion-on [data-rose-reveal]:not(.rose-in-view) {
    opacity: 0;
    transform: translate3d(0, 27px, 0);
  }
  html.rose-motion-on [data-rose-reveal].rose-in-view {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
  /* Preserve product hover lift after a scroll reveal has settled. */
  html.rose-motion-on .product-card.rose-in-view:hover {
    transform: translate3d(0, -5px, 0);
  }
  /* The existing favorite hero photograph remains fully unchanged. */
  html.rose-motion-on .hero-copy > .hero-eyebrow {
    animation: rose-arrive .70s .05s both var(--rose-ease);
  }
  html.rose-motion-on .hero-copy > h1 {
    animation: rose-arrive .90s .15s both var(--rose-ease);
  }
  html.rose-motion-on .hero-copy > p {
    animation: rose-arrive .90s .28s both var(--rose-ease);
  }
  html.rose-motion-on .hero-buttons {
    animation: rose-arrive .92s .38s both var(--rose-ease);
  }
  html.rose-motion-on .hero-footnote {
    animation: rose-arrive .92s .48s both var(--rose-ease);
  }
  html.rose-motion-on .hero-image-wrap {
    animation: rose-photo-arrive 1.18s .15s both var(--rose-ease);
  }
  html.rose-motion-on .hero-float-tag {
    animation: rose-arrive .85s .65s both var(--rose-ease);
  }
  @keyframes rose-arrive {
    from { opacity: 0; transform: translate3d(0, 25px, 0); }
    to { opacity: 1; transform: translate3d(0, 0, 0); }
  }
  @keyframes rose-photo-arrive {
    from { opacity: 0; transform: translate3d(0, 18px, 0) scale(.985); }
    to { opacity: 1; transform: translate3d(0, 0, 0) scale(1); }
  }
  @keyframes rose-menu-open {
    from { opacity: 0; transform: translate3d(0, -12px, 0); }
    to { opacity: 1; transform: translate3d(0, 0, 0); }
  }
  @keyframes rose-dialog-open {
    from { opacity: 0; transform: translate3d(0, 20px, 0) scale(.985); }
    to { opacity: 1; transform: translate3d(0, 0, 0) scale(1); }
  }
  @keyframes rose-overlay-open { from { opacity: 0; } to { opacity: 1; } }
  .mobile-menu.open { animation: rose-menu-open .35s var(--rose-ease) both; }
  .product-dialog[open] { animation: rose-dialog-open .46s var(--rose-ease) both; }
  .product-dialog[open]::backdrop { animation: rose-overlay-open .38s ease both; }
  .product-card,
  .occasion-card,
  .journal-card,
  .flower-type,
  .button,
  .filter-chip,
  .type-chip {
    -webkit-tap-highlight-color: transparent;
  }
  @media (hover: hover) and (pointer: fine) {
    .occasion-card img { transition: transform 1.05s var(--rose-ease), filter .5s ease; }
    .occasion-card:hover img, .occasion-card:focus-visible img {
      transform: scale(1.065);
      filter: saturate(1.04);
    }
    .occasion-caption b, .journal-read, .text-link span,
    .product-card .corner-arrow, .card-action > span {
      transition: transform .45s var(--rose-ease);
    }
    .occasion-card:hover .occasion-caption b,
    .journal-card:hover .journal-read,
    .product-card:hover .corner-arrow,
    .product-card:hover .card-action > span,
    .text-link:hover span {
      transform: translate3d(4px, -2px, 0);
    }
    .product-card { transition: transform .45s var(--rose-ease), box-shadow .45s ease, border-color .45s ease; }
    .product-card:hover, .product-card:focus-visible {
      border-color: #d6b6b5;
      box-shadow: 0 18px 48px rgba(88, 43, 55, .13);
    }
    .journal-photo { overflow: hidden; }
    .journal-photo img { transition: transform 1.05s var(--rose-ease); }
    .journal-card:hover .journal-photo img, .journal-card:focus-visible .journal-photo img {
      transform: scale(1.055);
    }
    .desktop-nav .nav-link:not(.active) {
      background-image: linear-gradient(#9c6476, #9c6476);
      background-size: 0 1px;
      background-repeat: no-repeat;
      background-position: left bottom;
      transition: color .25s, background-size .35s var(--rose-ease);
      padding-block: 5px;
    }
    .desktop-nav .nav-link:not(.active):hover,
    .desktop-nav .nav-link:not(.active):focus-visible {
      background-size: 100% 1px;
    }
  }
}

/* A tiny reading/progress accent for lengthy catalog or editorial pages. */
.rose-scroll-progress {
  position: fixed; top: 0; left: 0; z-index: 200;
  width: 100%; height: 2px; pointer-events: none;
  transform-origin: left center; transform: scaleX(0);
  background: linear-gradient(90deg, #bc8495, #722a46);
  opacity: .92;
}
@media (prefers-reduced-motion: reduce) {
  html.rose-motion-on [data-rose-reveal],
  html.rose-motion-on .hero-copy > *,
  html.rose-motion-on .hero-image-wrap,
  html.rose-motion-on .hero-float-tag,
  .mobile-menu.open, .product-dialog[open], .product-dialog[open]::backdrop {
    animation: none !important; transition: none !important;
    opacity: 1 !important; transform: none !important;
  }
  .marquee-track { animation: none !important; }
  .rose-scroll-progress { display: none; }
}
@media (hover: none), (pointer: coarse) {
  .product-card:hover, .occasion-card:hover img, .journal-card:hover img {
    transform: none;
  }
}
'''

css += r'''
/* ROSE-CO-EDITORIAL-MOTION-v2
   High-end motion details. Animated only on capable, motion-enabled devices. */
@media (prefers-reduced-motion: no-preference) {
  /* Slow, subtle atmospheric highlight, without ever replacing the hero photo. */
  .hero::before {
    content: "";
    position: absolute;
    inset: -18% -5%;
    z-index: -1;
    pointer-events: none;
    background:
      radial-gradient(ellipse at 11% 26%, rgba(255, 255, 255, .48), transparent 38%),
      radial-gradient(ellipse at 85% 83%, rgba(197, 127, 147, .16), transparent 45%);
    animation: rose-ambient 15s ease-in-out infinite alternate;
  }
  @keyframes rose-ambient {
    from { opacity: .65; transform: translate3d(-1%,0,0) scale(1); }
    to { opacity: 1; transform: translate3d(1%,1%,0) scale(1.035); }
  }
  /* Allow the hero message to arrive in a pleasant editorial rhythm. */
  html.rose-motion-on .hero-copy > h1 { animation-duration: 1.02s; }
  html.rose-motion-on .hero-image-wrap { animation-duration: 1.28s; }
  html.rose-motion-on .hero-float-tag {
    animation: rose-arrive .85s .65s both var(--rose-ease),
               rose-tag-breathe 7s 1.7s ease-in-out infinite alternate;
  }
  @keyframes rose-tag-breathe {
    from { translate: 0 0; }
    to { translate: 0 -5px; }
  }
  /* Fine calligraphic underline that draws in when a heading is revealed. */
  .section-head h2::after {
    content: "";
    display: block;
    width: min(82px, 28%);
    height: 1px;
    margin: 20px 0 0;
    transform-origin: left;
    transform: scaleX(0);
    background: linear-gradient(90deg, #b18679, #d9b5af);
    transition: transform 1.04s .20s var(--rose-ease);
  }
  .section-head.centered h2::after { margin-inline: auto; transform-origin: center; }
  .section-head.rose-in-view h2::after { transform: scaleX(1); }
  /* Refined interactive image reflections, limited to mouse/trackpad. */
  @media (hover: hover) and (pointer: fine) {
    .product-card .card-image::before {
      content:""; position:absolute; z-index:2; inset:0; pointer-events:none;
      background:linear-gradient(112deg, transparent 25%, rgba(255,255,255,.18) 46%, transparent 66%);
      transform:translate3d(-150%,0,0) skewX(-11deg);
      transition:transform 1.05s var(--rose-ease);
    }
    .product-card:hover .card-image::before,
    .product-card:focus-visible .card-image::before {
      transform:translate3d(150%,0,0) skewX(-11deg);
    }
    .journal-card .journal-photo img, .spotlight-gallery img {
      transition:transform 1.15s var(--rose-ease), filter .6s ease;
    }
    .journal-card:hover .journal-photo img { transform: scale(1.045); }
    .spotlight-gallery:hover img { transform: scale(1.025); }
    .filter-chip, .type-chip {
      transition: color .22s, background .22s, border-color .22s, transform .35s var(--rose-ease);
    }
    .filter-chip:hover, .type-chip:hover { transform: translate3d(0,-2px,0); }
    .journal-read { display:inline-flex; align-items:center; }
    .journal-card:hover .journal-read { color:var(--wine); }
  }
  /* Micro feedback on taps, without a continuous hover animation. */
  .button:active, .filter-chip:active, .type-chip:active {
    transform: scale(.985);
    transition-duration: .12s;
  }
  /* No abrupt modal appearance when inspecting flowers or gifts. */
  .product-dialog[open] .modal-photo img {
    animation: rose-modal-image .78s .11s both var(--rose-ease);
  }
  @keyframes rose-modal-image {
    from { opacity:.6; transform: scale(1.025); }
    to { opacity:1; transform: scale(1); }
  }
}
/* Opt out of nonessential ambient motion on small screens and touch devices. */
@media (max-width: 640px) {
  .hero::before { animation:none !important; }
  html.rose-motion-on .hero-float-tag {
    animation:rose-arrive .7s .35s both var(--rose-ease);
  }
  html.rose-motion-on [data-rose-reveal] {
    transition-duration:.64s,.72s;
  }
  html.rose-motion-on [data-rose-reveal]:not(.rose-in-view) {
    transform: translate3d(0,18px,0);
  }
}
@media (prefers-reduced-motion: reduce) {
  .hero::before { animation:none !important; }
  .section-head h2::after { transform:none !important; transition:none !important; }
  .product-dialog[open] .modal-photo img { animation:none !important; }
}
'''

js = r'''(() => {
  "use strict";
  // The page remains perfectly readable without animation-capable JavaScript.
  if (!("IntersectionObserver" in window) ||
      !("matchMedia" in window) ||
      !("requestAnimationFrame" in window) ||
      matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const selector = [
    ".section-head", ".occasion-card", ".product-card",
    ".spotlight-gallery", ".spotlight-copy", ".flower-type",
    ".journal-card", ".contact-grid > *", ".about-grid > *",
    ".article-photo", ".article-body > h2", ".article-body > h3",
    ".article-body > p", ".page-intro > .container > *",
    ".article-hero > h1", ".article-hero > p", ".article-return > *",
    ".seo-section-title"
  ].join(", ");
  const items = [...document.querySelectorAll(selector)];
  if (!items.length && !document.querySelector(".hero")) return;

  // A restrained 70 ms rhythm for card rows. Items further down the catalog
  // do not accumulate increasingly long delays.
  const staggerClass = [".occasion-card", ".product-card", ".flower-type", ".journal-card"];
  for (const node of items) {
    node.dataset.roseReveal = "";
    if (staggerClass.some(s => node.matches(s))) {
      let place = 0;
      let sibling = node.previousElementSibling;
      while (sibling && place < 3) {
        if (sibling.classList.contains(node.classList[0])) place++;
        sibling = sibling.previousElementSibling;
      }
      node.style.setProperty("--rose-delay", (place * 70) + "ms");
    }
    // Everything already onscreen stays immediately readable.
    const rect = node.getBoundingClientRect();
    if (rect.top < window.innerHeight + 32 && rect.bottom > -20) {
      node.classList.add("rose-in-view");
    }
  }
  document.documentElement.classList.add("rose-motion-on");

  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add("rose-in-view");
      observer.unobserve(entry.target);
    }
  }, {rootMargin: "0px 0px -20px 0px", threshold: .06});

  for (const node of items) {
    if (!node.classList.contains("rose-in-view")) observer.observe(node);
  }
  // Filtering catalogs can reveal a formerly hidden product. Make sure that
  // new result cards never remain transparent after user interaction.
  const catalog = document.querySelector("#catalog-grid");
  if (catalog) {
    const showVisible = () => {
      for (const card of catalog.querySelectorAll(".product-card:not([hidden])")) {
        if (card.getBoundingClientRect().top < innerHeight + 80)
          card.classList.add("rose-in-view");
      }
    };
    document.querySelectorAll(".filter-chip").forEach(chip =>
      chip.addEventListener("click", () => requestAnimationFrame(showVisible)));
    document.querySelector("#catalog-search")?.addEventListener("input", () =>
      requestAnimationFrame(showVisible));
  }

  // Very thin, passive page-position indicator on longer pages.
  let progress = null, queued = false;
  const render = () => {
    queued = false;
    if (!progress) return;
    const length = document.documentElement.scrollHeight - innerHeight;
    const fraction = length > 0 ? Math.max(0, Math.min(1, scrollY / length)) : 0;
    progress.style.transform = "scaleX(" + fraction + ")";
  };
  const update = () => {
    if (!queued) { queued = true; requestAnimationFrame(render); }
  };
  if (document.documentElement.scrollHeight > innerHeight * 1.55) {
    progress = document.createElement("div");
    progress.className = "rose-scroll-progress";
    progress.setAttribute("aria-hidden", "true");
    document.body.appendChild(progress);
    addEventListener("scroll", update, {passive: true});
    addEventListener("resize", update, {passive: true});
    render();
  }
  addEventListener("pageshow", () => {
    for (const node of items) {
      const rect = node.getBoundingClientRect();
      if (!node.hidden && rect.top < innerHeight + 40 && rect.bottom > -20)
        node.classList.add("rose-in-view");
    }
    update();
  });
})();'''

old_css = css_path.read_text(encoding="utf-8")
if css_marker not in old_css:
    css_path.write_text(old_css + "\n" + css, encoding="utf-8")
js_path.write_text(js, encoding="utf-8")

changed = 0
tag = '<script defer src="/rose-and-co/assets/rose-motion.js?v=motion2"></script>'
for page in root.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    if 'rose-motion.js' not in html:
        if "</head>" not in html:
            raise RuntimeError(f"Missing closing head: {page}")
        html = html.replace("</head>", tag + "</head>", 1)
    # Refresh stale GitHub Pages CSS and JS caches without touching images.
    html = re.sub(r'(/rose-and-co/assets/styles\.css)(?:\?v=[\w-]+)?',
                  r'\1?v=motion2', html)
    html = re.sub(r'/rose-and-co/assets/rose-motion\.js(?:\?v=[\w-]+)?',
                  '/rose-and-co/assets/rose-motion.js?v=motion2', html)
    page.write_text(html, encoding="utf-8")
    changed += 1

print(f"Rose & Co premium animations installed: {changed} pages, reduced motion supported.")
