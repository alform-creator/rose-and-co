(() => {
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
})();