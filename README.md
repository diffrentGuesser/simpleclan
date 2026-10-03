# SimpleClan website

The site for **SimpleClan**, a server-side Fabric mod for Minecraft 26.x, hosted
on GitHub Pages. This repository contains only the public website and the public
mod download — no private or admin tooling.

Live: https://diffrentguesser.github.io/simpleclan/

## Updating the downloadable jar

1. Build the public jar yourself (`gradlew :simpleclan:build` in the mod project).
2. Put `simple-clan-<version>.jar` into the [`jars/`](jars/) folder and commit it
   (drag-and-drop works: **Add file -> Upload files** on GitHub).
3. The **Update download from jars/** Action promotes it, updates the version and
   checksum on the page, and empties `jars/`. Pages redeploys automatically.

The Action refuses any jar that contains the private admin kit, so only clean
public builds can ever go live.

## Layout

- `index.html`, `source.html`, `style.css`, `main.js`, `source.js` — the site.
- `assets/` — icon, link-preview image, pixel art and fonts.
- `downloads/` — the current public jar (served as the download).
- `jars/` — drop a new version here to publish it.
- `tools/update_download.py` — the promotion script (runs in the Action; also
  runnable locally).

SimpleClan by Oakbanner. All rights reserved. Not an official Minecraft product.
