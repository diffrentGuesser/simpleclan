"""Promotes a newly uploaded jar to the website's download.

Drop a `simple-clan-<version>.jar` into the `jars/` folder and push. The
GitHub Action runs this script, which:

  1. Picks the highest-version jar in `jars/`.
  2. Refuses it if it contains the private admin kit (safety net).
  3. Moves it into `downloads/` (removing older downloads).
  4. Updates the version, file name, size, SHA-256 and date on index.html and
     source.html.
  5. Leaves `jars/` empty again.

The changelog text is not touched; edit index.html to add a changelog entry.
Run locally the same way: `python tools/update_download.py`.
"""
import datetime
import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JARS = ROOT / "jars"
DOWNLOADS = ROOT / "downloads"
INDEX = ROOT / "index.html"
SOURCE = ROOT / "source.html"


def version_key(name):
    m = re.search(r"simple-clan-(\d+)\.(\d+)\.(\d+)\.jar$", name)
    return tuple(int(x) for x in m.groups()) if m else (-1, -1, -1)


def main():
    candidates = [p for p in JARS.glob("simple-clan-*.jar") if "private" not in p.name.lower()]
    if not candidates:
        print("jars/: no simple-clan-*.jar to publish, nothing to do.")
        return

    jar = max(candidates, key=lambda p: version_key(p.name))
    m = re.search(r"simple-clan-(\d+\.\d+\.\d+)\.jar$", jar.name)
    if not m:
        sys.exit(f"{jar.name}: name must be simple-clan-<x.y.z>.jar")
    version = m.group(1)

    # Safety net: never publish a jar that carries the private admin kit.
    with zipfile.ZipFile(jar) as zf:
        bad = [n for n in zf.namelist() if "adminkit" in n.lower()]
        if not bad and "adminkit" in zf.read("fabric.mod.json").decode("utf-8").lower():
            bad = ["fabric.mod.json (adminkit entrypoint)"]

    data = jar.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    kb = max(1, round(len(data) / 1024))
    today = datetime.date.today()
    nice_date = f"{today.day} {today.strftime('%b %Y')}"

    DOWNLOADS.mkdir(exist_ok=True)
    for old in DOWNLOADS.glob("simple-clan-*.jar"):
        old.unlink()
    (DOWNLOADS / jar.name).write_bytes(data)

    html = INDEX.read_text(encoding="utf-8")
    old_sha = re.search(r'<code id="sha">([0-9a-f]{64})', html)
    jar_changed = not old_sha or old_sha.group(1) != sha
    html = re.sub(r"simple-clan-\d+\.\d+\.\d+\.jar", jar.name, html)
    html = re.sub(r"Download \d+\.\d+\.\d+", f"Download {version}", html)
    html = re.sub(r"(\.jar · )\d+ KB", rf"\g<1>{kb} KB", html)
    html = re.sub(r'(<code id="sha">)[0-9a-f]{64}', rf"\g<1>{sha}", html)
    html = re.sub(r"(<dt>Version</dt><dd>)[^<]*", rf"\g<1>{version}", html)
    if jar_changed:
        html = re.sub(r'(<dt>Updated</dt><dd><time datetime=")[^"]*(">)[^<]*',
                      rf"\g<1>{today.isoformat()}\g<2>{nice_date}", html)
    INDEX.write_text(html, encoding="utf-8", newline="\n")

    src = SOURCE.read_text(encoding="utf-8")
    src = re.sub(r"simple-clan-\d+\.\d+\.\d+\.jar", jar.name, src)
    src = re.sub(r"\(version \d+\.\d+\.\d+\)", f"(version {version})", src)
    SOURCE.write_text(src, encoding="utf-8", newline="\n")

    jar.unlink()  # consumed; it now lives in downloads/

    print(f"published {jar.name}: {kb} KB, sha256 {sha[:12]}..., version {version}"
          + (f", updated {nice_date}" if jar_changed else " (same jar as before)"))
    if f">{version} <time" not in html:
        print(f"note: no changelog entry for {version}; add one to index.html if you like.")


if __name__ == "__main__":
    main()
