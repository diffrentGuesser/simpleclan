# Drop new versions here

Put a public build named `simple-clan-<version>.jar` (for example
`simple-clan-1.2.3.jar`) in this folder and commit it.

A GitHub Action will:

1. Check the jar is a public build (it refuses anything containing the admin kit).
2. Move it into `../downloads/` as the file people download.
3. Update the version, size and checksum shown on the site.
4. Empty this folder again.

The website (GitHub Pages) then redeploys on its own. To add a changelog line,
edit `index.html` yourself.

Only one jar needs to be here at a time. If several are present, the highest
version wins.
