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