#!/usr/bin/env bash
set -e

# Build OSM2Syntax for Linux using PyInstaller
# Usage: ./build_linux.sh

if ! python3 - <<'PY'
import tkinter
PY
then
  echo "Error: Python cannot import tkinter."
  echo "On Arch Linux, install it with: sudo pacman -S --needed tk"
  exit 1
fi

python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt -r requirements-dev.txt

# Include fonts and key images in the bundle
PYINSTALLER=.venv/bin/pyinstaller

$PYINSTALLER --noconfirm --clean --onefile --windowed \
  --add-data "fonts:fonts" \
  --add-data "icon_clear.png:." \
  --add-data "icon_download.png:." \
  --add-data "logo_txt_black.png:." \
  --add-data "logo_txt_white.png:." \
  --add-data "icon_sun.png:." \
  --add-data "icon_moon.png:." \
  --add-data "icon_preview.png:." \
  --add-data "icon_savepreview.png:." \
  --add-data "icon_cancel.png:." \
  --add-data "icon_br.png:." \
  --add-data "icon_uk.png:." \
  --add-data "icon.ico:." \
  --collect-binaries pyogrio \
  --collect-data pyogrio \
  --hidden-import "PIL._tkinter_finder" \
  --hidden-import "pyogrio._err" \
  --hidden-import "pyogrio._geometry" \
  --hidden-import "pyogrio._io" \
  --hidden-import "pyogrio._ogr" \
  --hidden-import "pyogrio._vsi" \
  --copy-metadata osmnx \
  --copy-metadata geopandas \
  --copy-metadata pandas \
  --copy-metadata shapely \
  --copy-metadata pyproj \
  --copy-metadata pyogrio \
  osm2syntax.py

echo "Build complete: dist/osm2syntax"
