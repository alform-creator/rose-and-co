(() => {
  "use strict";
  const stage = document.getElementById("rose-runner");
  if (!stage) return;

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const intervalMs = 30000;  // Every thirty seconds after the first preview
  const durationMs = 6500;
  const closeButton = stage.querySelector(".rose-runner-close");
  const replay = new URLSearchParams(location.search).get("animation") === "1";
  let dismissed = reduced.matches;
  try { dismissed = dismissed || (!replay && sessionStorage.getItem('rose-runner-dismissed') === '1'); } catch {}
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
    // Start after the intro; subsequent appearances keep their 30-second cycle.
    const delay = 6500;
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
})();
