#!/usr/bin/env bash
# Render both pages with headless Chrome and compose the side-by-side image.
# Needs Google Chrome and ImageMagick (magick).
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size="$2" \
           --screenshot="$PWD/$3" "file://$PWD/$1" 2>/dev/null; }
# page:body-background pairs; the background is needed to re-pad after trimming.
for entry in with-skill:white without-skill:#f4f6f9; do
  page="${entry%%:*}" bg="${entry#*:}"
  shot "$page.html" 1440,900  "$page-fold.png"
  shot "$page.html" 1440,4200 "$page-full.png"
  # Chrome has no full-page flag: render tall, then cut the blank tail.
  magick "$page-full.png" -fuzz 1% -trim +repage -gravity north -background "$bg" \
         -extent 1440x -splice 0x40 -gravity south -splice 0x40 "$page-full.png"
done
magick without-skill-fold.png with-skill-fold.png -bordercolor '#ddd' -border 1 +append side-by-side.png
echo "wrote side-by-side.png and *-fold.png, *-full.png"
