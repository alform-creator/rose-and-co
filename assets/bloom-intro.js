(() => {
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
})();
