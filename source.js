// Copy a source file to the clipboard. The code element holds one line per
// child row; reading textContent gives back the plain source without the
// line-number markers (those are CSS-generated).
document.querySelectorAll(".src-copy").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const code = document.getElementById("code-" + btn.dataset.file);
    const label = btn.querySelector("span");
    try {
      await navigator.clipboard.writeText(code.innerText.replace(/​/g, ""));
      label.textContent = "Copied";
      btn.classList.add("done");
    } catch {
      label.textContent = "Copy failed";
    }
    setTimeout(() => { label.textContent = "Copy"; btn.classList.remove("done"); }, 2000);
  });
});
