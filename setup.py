from cx_Freeze import setup, Executable
import sys

# Dependências que o programa usa
packages = [
    "os",
    "re",
    "threading",
    "time",
    "unicodedata",
    "webbrowser",
    "datetime",
    "tkinter",
    "matplotlib",
    "networkx",
    "numpy",
    "osmnx",
    "ttkbootstrap",
    "PIL",
    "shapely"
]

# Arquivos extras que precisam ir para o executável
include_files = [
    ("fonts", "fonts"),

    "icon.ico",
    "icon_clear.png",
    "icon_download.png",
    "icon_sun.png",
    "icon_moon.png",
    "icon_preview.png",
    "icon_savepreview.png",
    "icon_cancel.png",
    "icon_br.png",
    "icon_uk.png",

    "logo_txt_black.png",
    "logo_txt_white.png"
]

build_exe_options = {
    "packages": packages,
    "include_files": include_files,
    "excludes": ["tkinter.test"],
}

# Para aplicações com interface gráfica
base = None
if sys.platform == "win32":
    base = "gui"

executables = [
]

# Ajusta nome do executável e ícone conforme plataforma
target_name = "OSM2Syntax.exe" if sys.platform == "win32" else "OSM2Syntax"
icon_arg = {"icon": "icon.ico"} if sys.platform == "win32" else {}

executables = [
    Executable(
        "osm2syntax.py",
        base=base,
        target_name=target_name,
        **icon_arg
    )
]
]

setup(
    name="OSM2Syntax",
    version="1.0.4",
    description="OSM2Syntax 1.0.4",
    options={"build_exe": build_exe_options},
    executables=executables
)