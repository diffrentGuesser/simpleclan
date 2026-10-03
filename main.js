// Locator bar demo: switch modes and hide the dots Steve wouldn't see.
const locator = document.querySelector(".locator");
if (locator) {
  const buttons = locator.querySelectorAll("[data-set]");
  const shown = locator.querySelectorAll("[data-show]");
  const bar = locator.querySelector(".bar");

  const apply = (mode) => {
    locator.dataset.mode = mode;
    let visible = 0;
    shown.forEach((el) => {
      const on = el.dataset.show.split(" ").includes(mode);
      el.classList.toggle("off", !on);
      if (on && el.classList.contains("dot")) visible++;
    });
    buttons.forEach((b) => {
      const active = b.dataset.set === mode;
      b.setAttribute("aria-checked", String(active));
      b.tabIndex = active ? 0 : -1;
    });
    bar.setAttribute("aria-label",
      visible === 0 ? "Steve's locator bar showing no players"
                    : `Steve's locator bar showing ${visible} player${visible === 1 ? "" : "s"}`);
  };

  buttons.forEach((b) => b.addEventListener("click", () => apply(b.dataset.set)));
  // Arrow keys move between the three modes, like a native radio group.
  locator.querySelector(".seg").addEventListener("keydown", (e) => {
    if (!["ArrowLeft", "ArrowRight"].includes(e.key)) return;
    const list = [...buttons];
    const i = list.findIndex((b) => b.getAttribute("aria-checked") === "true");
    const next = list[(i + (e.key === "ArrowRight" ? 1 : list.length - 1)) % list.length];
    apply(next.dataset.set);
    next.focus();
    e.preventDefault();
  });
  apply(locator.dataset.mode);
}

// Copy the SHA-256 hash.
document.querySelectorAll("[data-copy]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const text = document.querySelector(btn.dataset.copy).textContent.trim();
    const label = btn.querySelector("span");
    try {
      await navigator.clipboard.writeText(text);
      label.textContent = "Copied";
      btn.classList.add("done");
    } catch {
      label.textContent = "Copy failed, select the hash instead";
    }
    setTimeout(() => { label.textContent = "Copy hash"; btn.classList.remove("done"); }, 2000);
  });
});

// Highlight the tab for the section in view.
const tabs = document.querySelectorAll(".tabs a");
const sections = [...tabs].map((a) => document.querySelector(a.getAttribute("href")));
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    tabs.forEach((a) => a.classList.toggle("on", a.getAttribute("href") === `#${entry.target.id}`));
  });
}, { rootMargin: "-30% 0px -60% 0px" });
sections.forEach((s) => s && observer.observe(s));
