# OSM2Syntax — Build e Teste em Linux

Este repositório contém o aplicativo OSM2Syntax (originalmente com build para Windows). Aqui estão os passos para gerar e testar um build Linux usando um ambiente virtual.

Pré-requisitos
- Python 3.8+ instalado
- `git` (opcional)
- em SSH headless, instale `xvfb` para testes GUI: `sudo apt install xvfb`

Passos para criar o build (recomendado)

1. Criar virtualenv e ativar

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

2. Instalar dependências

```bash
python -m pip install -r requirements.txt pyinstaller
```

3. Gerar o executável (script preparado)

```bash
./build_linux.sh
```

O executável gerado ficará em `dist/osm2syntax`.

Comandos alternativos (mais verbosos)

```bash
.venv/bin/pyinstaller --noconfirm --onefile --windowed \
  --hidden-import PIL._tkinter_finder --hidden-import PIL.ImageTk \
  --add-data "fonts:fonts" --add-data "icon_clear.png:." --add-data "icon_download.png:." \
  --add-data "logo_txt_black.png:." --add-data "logo_txt_white.png:." --add-data "icon_sun.png:." \
  --add-data "icon_moon.png:." --add-data "icon_preview.png:." --add-data "icon_savepreview.png:." \
  --add-data "icon_cancel.png:." --add-data "icon_br.png:." --add-data "icon_uk.png:." --add-data "icon.ico:." \
  --copy-metadata osmnx --copy-metadata geopandas --copy-metadata pandas --copy-metadata shapely \
  --copy-metadata pyproj --copy-metadata pyogrio \
  osm2syntax.py
```

Testes (GUI)
- Com display local: `./dist/osm2syntax`
- Em SSH sem DISPLAY: instale `xvfb` e rode:

```bash
sudo apt install xvfb
xvfb-run -s "-screen 0 1024x768x24" ./dist/osm2syntax
```

Depuração (mais direta)
- Rodar o script com o Python do venv expõe tracebacks completos:

```bash
. .venv/bin/activate
xvfb-run -s "-screen 0 1024x768x24" .venv/bin/python osm2syntax.py
```

Erros comuns e correções rápidas
- `No package metadata was found for ...`: adicionar `--copy-metadata <package>` ao PyInstaller.
- `FileNotFoundError` para ícones/fonts: garantir `--add-data` e que `osm2syntax.py` usa `sys._MEIPASS` quando frozen (já ajustado).
- PIL/ImageTk ModuleNotFoundError: passar `--hidden-import PIL._tkinter_finder --hidden-import PIL.ImageTk`.
- Sem `$DISPLAY`: usar `xvfb-run`.

Commit sugerido

```bash
git add setup.py osm2syntax.py requirements.txt build_linux.sh .gitignore README.md
git commit -m "Add Linux build support: PyInstaller script, cross-platform resources and docs"
git push
```

Se quiser, eu também posso criar um pacote `.deb` ou um `AppImage` posteriormente. Se testar e encontrar erros, copie/cole a saída do terminal aqui e eu ajudo a depurar.
# OSM2Syntax

**Road-Center Line Preparation Tool for Space Syntax Analysis**

OSM2Syntax is a desktop application developed in Python that allows users to download, process, and simplify road networks from OpenStreetMap for use in **Space Syntax analysis** and other spatial network studies.

The software provides a graphical interface that enables users to retrieve street networks, preview them, apply simplification techniques, and export the results as GIS-ready files.

---

## Features

- Download road centerline networks from **OpenStreetMap**
- Query data by:
  - Place name (via OSM Nominatim)
  - Geographic coordinates + radius
- Preview road networks before downloading
- Simplify road geometries using angular threshold and tolerance parameters
- Export road networks as **GeoPackage (.gpkg)**
- Optional background layers:
  - Buildings
  - Vegetation
  - Parks
  - Water bodies
- Generate automatic **download reports**
- Export preview images (PNG, JPG, PDF)
- Multithreaded download system
- Dark Mode / Light Mode
- Bilingual interface (English / Portuguese)

---

## Application Interface

The graphical interface allows users to:

1. Select a geographic reference (place name or coordinates)
2. Preview the road network
3. Configure simplification parameters
4. Select background layers
5. Download and export the processed data

---

## Installation

### Clone the repository

```bash
git clone https://github.com/alexbccastro/OSM2Syntax.git
cd OSM2Syntax
Create a virtual environment
python -m venv venv

Activate the environment

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Dependencies

Main libraries used in this project:

matplotlib

networkx

numpy

osmnx

ttkbootstrap

pillow

shapely

How to Use

Select the geographic reference:

Name (example: João Pessoa, Brazil)

Coordinates + radius

Click Preview to visualize the road network.

Optionally enable Simplify RCL and adjust parameters:

Angular Threshold

Tolerance

Select background layers if needed.

Choose the folder to save the data.

Click Download.

Output Files

The software generates:

rcl_location.gpkg
rcl_location_buildings.gpkg
rcl_location_vegetation.gpkg
rcl_location_park.gpkg
rcl_location_water.gpkg
rcl_location_report.txt

The report includes:

download date

network type

simplification parameters

vertex reduction metrics

length variation

download time

Preview Export

The preview map can be exported as:

PNG

JPEG

PDF

Technologies

Python

OpenStreetMap

OSMnx

NetworkX

Matplotlib

Tkinter

ttkbootstrap

Author

Alexandre Augusto Bezerra da Cunha Castro

March 2026

License

This project is licensed under the MIT License.