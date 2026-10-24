#!/usr/bin/env python3
"""Install light, accessible editorial motion across all Rose & Co pages.

Run after install-real-photos.py when the unpacked website is complete.
No external animation libraries, source-photo edits, or layout changes.
"""
from pathlib import Path
import sys

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

js = r'''(() => {
  "use strict";
  // Progressive enhancement only: static content stays visible without JS.
  if (!("IntersectionObserver" in window) ||
      !("matchMedia" in window) ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const selector = [
    ".section-head", ".occasion-card", ".product-card",
    ".spotlight-gallery", ".spotlight-copy", ".flower-type",
    ".journal-card", ".contact-grid > *", ".about-grid > *",
    ".article-photo", ".article-body > p",
    ".page-intro > .container > *", ".article-hero > h1",
    ".article-hero > p", ".article-return > *"
  ].join(", ");
  const items = [...document.querySelectorAll(selector)]
    .filter(node => !node.closest("[hidden]"));
  if (!items.length && !document.querySelector(".hero")) return;

  // Per-grid stagger gives order without making long pages feel slow.
  const staggerClasses = [".occasion-card", ".product-card", ".flower-type", ".journal-card"];
  items.forEach((node, index) => {
    node.setAttribute("data-rose-reveal", "");
    const grid = staggerClasses.some(s => node.matches(s));
    if (grid) {
      let position = 0;
      let previous = node.previousElementSibling;
      while (previous && position < 3) {
        if (previous.matches(node.tagName + "." + node.classList[0])) position++;
        previous = previous.previousElementSibling;
      }
      node.style.setProperty("--rose-delay", (position * 70) + "ms");
    }
    // Above-the-fold content should never start hidden.
    const bounds = node.getBoundingClientRect();
    if (bounds.top <= window.innerHeight + 30 && bounds.bottom >= -25) {
      node.classList.add("rose-in-view");
    }
  });
  document.documentElement.classList.add("rose-motion-on");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("rose-in-view");
      observer.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -26px 0px", threshold: .06 });
  items.forEach(node => {
    if (!node.classList.contains("rose-in-view")) observer.observe(node);
  });

  // Visible, discreet page position — only on long pages.
  let progress;
  let pending = false;
  function updateProgress() {
    pending = false;
    if (!progress) return;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = "scaleX(" + (max > 0 ? Math.max(0, Math.min(1, window.scrollY / max)) : 0) + ")";
  }
  function scheduleProgress() {
    if (!pending) {
      pending = true;
      requestAnimationFrame(updateProgress);
    }
  }
  if (document.documentElement.scrollHeight > window.innerHeight * 1.55) {
    progress = document.createElement("div");
    progress.className = "rose-scroll-progress";
    progress.setAttribute("aria-hidden", "true");
    document.body.appendChild(progress);
    window.addEventListener("scroll", scheduleProgress, { passive: true });
    window.addEventListener("resize", scheduleProgress, { passive: true });
    updateProgress();
  }

  // Browser back/forward and filter changes must not leave cards hidden.
  window.addEventListener("pageshow", () => {
    items.forEach(node => {
      if (!node.hidden && node.getBoundingClientRect().top < window.innerHeight + 30 &&
          node.getBoundingClientRect().bottom > -25) node.classList.add("rose-in-view");
    });
    scheduleProgress();
  });
})();
'''

old_css = css_path.read_text(encoding="utf-8")
if css_marker not in old_css:
    css_path.write_text(old_css + "\n" + css, encoding="utf-8")
js_path.write_text(js, encoding="utf-8")

changed = 0
tag = '<script defer src="/rose-and-co/assets/rose-motion.js?v=motion1"></script>'
for page in root.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    if 'rose-motion.js' not in html:
        if "</head>" not in html:
            raise RuntimeError(f"Missing closing head: {page}")
        html = html.replace("</head>", tag + "</head>", 1)
    # Change ONLY the stylesheet version, never the image/hero URLs.
    html = html.replace("styles.css?v=align6", "styles.css?v=motion1")
    page.write_text(html, encoding="utf-8")
    changed += 1

print(f"Rose & Co premium animations installed: {changed} pages, reduced motion supported.")
