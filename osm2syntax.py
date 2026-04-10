# Standard Library
import os
import re
import threading
import time
import unicodedata
import webbrowser
from datetime import datetime
from tkinter import filedialog, messagebox
from ctypes import windll
import sys

# Third-Party Libraries
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import osmnx as ox
import ttkbootstrap as tb
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from shapely.geometry import LineString


ox.settings.overpass_endpoint = "https://overpass.kumi.systems/api/interpreter"
ox.settings.timeout = 180
ox.settings.headers = {"User-Agent": "OSM2Syntax/1.0"}


# Language System
LANG = {
    "en": {
        "download": "Download",
        "cancel": "Cancel",
        "clear": "Clear",
        "preview": "Preview",
        "plot": "Plot",
        "dark": "Dark Mode",
        "light": "Light Mode",
        "status_waiting": "Status: Waiting",
        "status_cancel": "Status: Cancelling download...",
        "name": "Name (OSM Nominatim)",
        "point": "Point (Decimal Degrees)",
        "radius": "Radius (m)",
        "simplify": "Simplify RCL",
        "angular_threshold": "Angle Threshold",
        "tolerance": "Tolerance",
        "buildings": "Buildings",
        "nature": "Nature",
        "park": "Park",
        "water": "Water",
        "saveas": "Folder to Save the Data",
        "empty_name": "Place name cannot be empty.",
        "error_name": "Invalid place name. Please check OSM Nominatim.",
        "error_latlongrad": "Latitude, Longitude and Radius must be numeric.",
        "error_lat": "Latitude must be between -90 and 90.",
        "error_long": "Longitude must be between -180 and 180.",
        "error_rad": "Radius must be greater than zero.",
        "error_coord_query": "Invalid coordinate query.",
        "error_name_point": "Select Name or Point.",
        "cancelled": "CANCELLED",
        "report_title": "OSM2Syntax – Download Report",
        "date": "Date",
        "location": "Location",
        "network_type": "Network Type",
        "simplified": "Simplified",
        "original": "Original",
        "file": "File",
        "file_size": "File Size",
        "download_time": "Download Time",
        "seconds": "seconds",
        "background_layers": "Background Layers",
        "none": "None",
        "metrics": "SIMPLIFICATION METRICS",
        "angle_threshold": "Angle Threshold",
        "vertices_before": "Vertices BEFORE",
        "vertices_after": "Vertices AFTER",
        "vertex_reduction": "Vertex Reduction (%)",
        "length_before": "Length BEFORE (m)",
        "length_after": "Length AFTER (m)",
        "length_variation": "Length Variation (%)",
        "Error": "Error",
        "download_cancelled": "Download cancelled.",
        "download_completed": "Download completed successfully!",
        "download_completed_title": "Download Completed",
        "preview_loading": "Loading preview...",
        "preview_loaded": "Preview loaded successfully.",
        "preview_none": "No preview loaded.",
        "status_processing": "Processing network...",
        "status_simplifying": "Applying simplification...",
        "status_saving": "Saving files...",
        "status_connecting": "Connecting to OSM...",
        "preview_error": "Preview Error",
        "menu": "Menu",
        "view": "View",
        "help": "Help",
        "about": "About OSM2Syntax",
        "github": 'OSM2Syntax on GitHub',
        "exit": "Exit",
        "dark_mode": "Toggle Dark Mode",
        "fullscreen": "Toggle Fullscreen",
        "btn_dark": "Dark Mode",
        "btn_light": "Light Mode",
        "quick_tutorial": "Quick Tutorial",
        "tutorial_text": """
        Quick Tutorial – OSM2Syntax

        1. Select the geographic reference (name or point) and fill in the corresponding fields;

        2. If you want to preview the place, click on "Preview". If you want to save it as a image, click on "Plot";

        3. If you want to simplify road geometries, click on "Simplify RCL". Change the parameters if you want;

        4. Select background layers if needed;

        5. Click on "..." to indicate the folder to save the data

        6. Click Download to retrieve the data.

        At the end, OSM2Syntax will generate the RCL file, background layers (if selected) and the download report.

        """,
        "about_text": """
        OSM2Syntax v.1.0.2

        Road-Center Line Preparation Tool for Space Syntax Analysis

        Powered by OSMnx
        Developed in Python

        Developer: Alexandre Augusto Bezerra da Cunha Castro
        March | 2026
        """,
        "tooltip_name": "Insert a valid name according to OSM Nominatim (e.g.: 'João Pessoa, Brazil')",
        "tooltip_point": "Insert latitude and longitude in decimal degrees (e.g.: -15.7939869, -47.8828000)",
        "tooltip_radius": "Data coverage radius (in meters) from the specified point coordinates.",
        "tooltip_simplify": "Removes redundant nodes to create a cleaner and lighter network structure.",
        "tooltip_angle": "Defines the angular limit (degrees) below which adjacent segments are considered aligned.",
        "tooltip_tolerance": "Maximum allowed deviation when simplifying geometry (map units).",
        "save_preview_as": "Save Preview As",
        "preview_saved_title": "Saved",
        "preview_saved_message": "Preview saved successfully!",
        "error_title": "Error",
        "status_prefix": "Status: "
    },

    "pt": {
        "download": "Baixar",
        "cancel": "Cancelar",
        "clear": "Limpar",
        "preview": "Visualizar",
        "plot": "Salvar",
        "status_waiting": "Status: Aguardando",
        "status_cancel": "Status: Cancelando download...",
        "name": "Nome (OSM Nominatim)",
        "point": "Ponto (Graus Decimais)",
        "radius": "Raio (m)",
        "simplify": "Simplificar RCL",
        "angular_threshold": "Limiar Angular",
        "tolerance": "Tolerância",
        "buildings": "Edificações",
        "nature": "Natureza",
        "park": "Praças",
        "water": "Água",
        "saveas": "Pasta para Salvar os Dados",
        "empty_name": "O campo do Nome não pode ficar vazio.",
        "error_name": "Nome inválido. Por favor, confira o OSM Nominatim.",
        "error_latlongrad": "Latitude, Longitude e Raio devem ser numéricos.",
        "error_lat": "Valor de Latitude deve ser entre -90 e 90.",
        "error_long": "Valor de Longitude deve ser entre -180 e 180.",
        "error_rad": "Raio deve ser maior que zero.",
        "error_coord_query": "Consulta de coordenada inválida.",
        "error_name_point": "Selecione Nome ou Ponto.",
        "cancelled": "CANCELADO",
        "report_title": "OSM2Syntax – Relatório de Download",
        "date": "Data",
        "location": "Local",
        "network_type": "Tipo de Rede",
        "simplified": "Simplificada",
        "original": "Original",
        "file": "Arquivo",
        "file_size": "Tamanho do Arquivo",
        "download_time": "Tempo de Download",
        "seconds": "segundos",
        "background_layers": "Camadas de Fundo",
        "none": "Nenhuma",
        "metrics": "MÉTRICAS DE SIMPLIFICAÇÃO",
        "angle_threshold": "Limiar Angular",
        "vertices_before": "Vértices ANTES",
        "vertices_after": "Vértices DEPOIS",
        "vertex_reduction": "Redução de Vértices (%)",
        "length_before": "Comprimento ANTES (m)",
        "length_after": "Comprimento DEPOIS (m)",
        "length_variation": "Variação de Comprimento (%)",
        "Error": "Erro",
        "download_cancelled": "Download cancelado.",
        "download_completed": "Download concluído com sucesso!",
        "download_completed_title": "Download Concluído",
        "preview_loading": "Carregando visualização...",
        "preview_loaded": "Visualização carregada com sucesso.",
        "preview_none": "Nenhuma visualização carregada.",
        "status_processing": "Processando rede...",
        "status_simplifying": "Aplicando simplificação...",
        "status_saving": "Salvando arquivos...",
        "status_connecting": "Conectando ao OSM...",
        "preview_error": "Erro na Visualização",
        "menu": "Menu",
        "view": "Visualizar",
        "help": "Ajuda",
        "about": "Sobre o OSM2Syntax",
        "github": 'Página do OSM2Syntax no GitHub',
        "exit": "Sair",
        "dark_mode": "Ativar Modo Escuro",
        "fullscreen": "Ativar Tela Cheia",
        "btn_dark": "Modo Escuro",
        "btn_light": "Modo Claro",
        "quick_tutorial": "Tutorial rápido",
        "tutorial_text": """
        Tutorial rápido – OSM2Syntax

        1. Selecione a referência geográfica (nome ou ponto) e preencha os campos correspondentes;

        2. Se quiser visualizar o local, clique em “Visualizar”. Se quiser guardá-lo como imagem, clique em “Salvar”;

        3. Se quiser simplificar a geometria das vias, clique em “Simplificar RCL”. Altere os parâmetros, se desejar;

        4. Selecione as camadas de fundo, se necessário;

        5. Clique em “...” para indicar a pasta onde deseja guardar os dados

        6. Clique em Download para recuperar os dados.

        No final, o OSM2 irá gerar o ficheiro de rede, as camadas de fundo (se selecionadas) e o relatório de download.

        """,
        "about_text": """
        OSM2Syntax v.1.0.2

        Ferramenta para preparação de Road-Center Line
        para análise em Sintaxe Espacial

        Baseado em OSMnx
        Desenvolvido em Python

        Desenvolvedor: Alexandre Augusto Bezerra da Cunha Castro
        Março | 2026
        """,
        "tooltip_name": "Insira um nome válido de acordo com o OSM Nominatim (ex.: 'João Pessoa, Brasil')",
        "tooltip_point": "Insira latitude e longitude em graus decimais (ex.: -15.7939869, -47.8828000)",
        "tooltip_radius": "Raio de cobertura dos dados (em metros) a partir do ponto informado.",
        "tooltip_simplify": "Remove nós redundantes para criar uma rede mais limpa e leve.",
        "tooltip_angle": "Define o limite angular (graus) abaixo do qual segmentos adjacentes são considerados alinhados.",
        "tooltip_tolerance": "Desvio máximo permitido ao simplificar a geometria.",
        "save_preview_as": "Salvar Visualiação Como",
        "preview_saved_title": "Salvo",
        "preview_saved_message": "Visualização salva com sucesso!",
        "error_title": "Erro",
        "status_prefix": "Status: ",
    }
}
current_lang = "en"
preview_state = "none"  # "none", "loading", "loaded"
cancel_event = threading.Event()


def apply_global_font():
    style.configure(".", font=("IBM Plex Sans Medium", 10))


def build_graph():
    custom_filter = ('["highway"~"motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|secondary_link'
                     '|tertiary|tertiary_link|residential|living_street|unclassified|road|pedestrian"]')

    simplify_flag = simplify_checkbutton_var.get()

    # Graph by name
    if name_checkbutton_var.get():
        place = name_entry.get().strip()

        if not place:
            raise ValueError(LANG[current_lang]["empty_name"])

        try:
            g = ox.graph_from_place(place, custom_filter=custom_filter, simplify=simplify_flag)
        except Exception:
            raise ValueError(LANG[current_lang]["error_name"])

    # Graph by point
    elif point_checkbutton_var.get():

        try:
            lat = float(lat_entry_var.get())
            lon = float(long_entry_var.get())
            radius = float(radius_entry_var.get())
        except ValueError:
            raise ValueError(LANG[current_lang]["error_latlongrad"])

        if not (-90 <= lat <= 90):
            raise ValueError(LANG[current_lang]["error_lat"])

        if not (-180 <= lon <= 180):
            raise ValueError(LANG[current_lang]["error_long"])

        if radius <= 0:
            raise ValueError(LANG[current_lang]["error_rad"])

        try:
            g = ox.graph_from_point((lat, lon), dist=radius, custom_filter=custom_filter,
                                    simplify=simplify_flag)
        except Exception:
            raise ValueError(LANG[current_lang]["error_coord_query"])

    else:
        raise ValueError(LANG[current_lang]["error_name_point"])

    return g


def build_graph_preview():
    custom_filter = ('["highway"~"motorway|trunk|primary|secondary|tertiary|residential|unclassified|pedestrian"]')

    # Graph preview by name
    if name_checkbutton_var.get():
        place = name_entry.get().strip()

        if not place:
            raise ValueError(LANG[current_lang]["empty_name"])

        try:
            g = ox.graph_from_place(place, custom_filter=custom_filter, simplify=True)
        except Exception:
            raise ValueError(LANG[current_lang]["error_name"])

    # Graph preview by point
    elif point_checkbutton_var.get():

        try:
            lat = float(lat_entry_var.get())
            lon = float(long_entry_var.get())
            radius = float(radius_entry_var.get())
        except ValueError:
            raise ValueError(LANG[current_lang]["error_latlongrad"])

        if radius <= 0:
            raise ValueError(LANG[current_lang]["error_rad"])

        try:
            g = ox.graph_from_point((lat, lon), dist=radius, custom_filter=custom_filter, simplify=False)
        except Exception:
            raise ValueError(LANG[current_lang]["error_coord_query"])

    else:
        raise ValueError(LANG[current_lang]["error_name_point"])

    g = g.to_undirected()
    largest_cc = max(nx.connected_components(g), key=len)
    g = g.subgraph(largest_cc).copy()
    g = ox.project_graph(g)
    return g


def check_cancel():
    if cancel_event.is_set():
        raise RuntimeError(LANG[current_lang]["cancelled"])


def cancel_download():
    cancel_event.set()
    status_txt.config(text=LANG[current_lang]["status_cancel"])


def check_download_ready():
    location_selected = name_checkbutton_var.get() or point_checkbutton_var.get()
    directory_selected = bool(saveas_entry_var.get())

    if location_selected and directory_selected:
        download_button.config(state="normal", cursor="hand2")
    else:
        download_button.config(state="disabled", cursor="arrow")

    if location_selected:
        preview_button.config(state="normal", cursor="hand2")
    else:
        preview_button.config(state="disabled", cursor="arrow")


def choose_directory():
    folder = filedialog.askdirectory()
    if folder:
        saveas_entry_var.set(folder)
    check_download_ready()


def clear_all():
    global preview_state
    preview_state = "none"

    name_checkbutton_var.set(False)
    point_checkbutton_var.set(False)
    simplify_checkbutton_var.set(False)

    name_entry.delete(0, tk.END)
    lat_entry_var.set("")
    long_entry_var.set("")
    radius_entry_var.set("")
    angle_threshold_var.set("")
    tolerance_var.set("")
    saveas_entry_var.set("")
    angle_threshold_var.set(5)
    tolerance_var.set(10)
    buildings_var.set(False)
    nature_var.set(False)
    park_var.set(False)
    water_var.set(False)
    toggle_name()
    toggle_point()
    toggle_simplify()

    progress_bar_var.set(0)
    status_txt.config(text=LANG[current_lang]["status_waiting"])
    download_button.config(state="disabled", cursor="arrow")

    fig.clear()

    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])

    if dark_mode_var.get():
        fig.patch.set_facecolor("#222222")
        ax.set_facecolor("#222222")
    else:
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

    canvas.draw()
    preview_status.config(text=LANG[current_lang]["preview_none"])
    preview_button.config(state="disabled", cursor="arrow")
    save_preview_button.config(state="disabled", cursor="arrow")


def create_custom_button_styles():
    # Directory Button
    style.configure("Directory.TButton", font=("IBM Plex Sans Medium", 10, "bold"), padding=8)

    # Clear Button
    style.configure("Clear.TButton", font=("IBM Plex Sans Medium", 10, "bold"), padding=8)

    # Download Button
    style.configure("Download.TButton", font=("IBM Plex Sans Medium", 11, "bold"), padding=10)


def download_data():
    threading.Thread(target=run_download, daemon=True).start()


def error_progress(message="Error"):
    global progress_state
    progress_state = "danger"
    progress_bar.stop()
    progress_bar.config(mode="determinate", bootstyle="danger")
    progress_bar_var.set(0)
    status_txt.config(text=f"{LANG[current_lang]['status_prefix']}{message}")
    download_button.config(state="normal", cursor="hand2")
    darktheme_button.config(state="normal")
    mainwindow.after(0, update_preview_button_state)
    clean_button.config(state="normal", cursor="hand2")
    preview_button.config(state="normal", cursor="hand2")
    cancel_button.config(state="disabled", cursor="arrow")


def exit_fullscreen(event=None):
    mainwindow.attributes("-fullscreen", False)


def finish_progress(message=None):
    global progress_state

    if message is None:
        message = LANG[current_lang]["download_completed"]

    progress_state = "success"
    progress_bar.stop()
    progress_bar.config(mode="determinate", bootstyle="success")
    progress_bar_var.set(100)

    status_txt.config(
        text=f"{LANG[current_lang]['status_prefix']}{message}"
    )

    download_button.config(state="normal", cursor="hand2")
    darktheme_button.config(state="normal", cursor="hand2")
    clean_button.config(state="normal", cursor="hand2")
    preview_button.config(state="normal", cursor="hand2")
    save_preview_button.config(state="normal", cursor="hand2")
    cancel_button.config(state="disabled", cursor="arrow")


def load_custom_font():
    FR_PRIVATE = 0x10

    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    font_path_regular = os.path.join(base_path, "fonts", "IBMPlexSans-Regular.ttf")
    font_path_medium = os.path.join(base_path, "fonts", "IBMPlexSans-Medium.ttf")

    if os.path.exists(font_path_regular):
        windll.gdi32.AddFontResourceExW(font_path_regular, FR_PRIVATE, 0)

    if os.path.exists(font_path_medium):
        windll.gdi32.AddFontResourceExW(font_path_medium, FR_PRIVATE, 0)


def make_safe_filename(text, max_length=80):
    # Remove accents
    normalized = unicodedata.normalize('NFKD', str(text))
    ascii_text = normalized.encode('ASCII', 'ignore').decode('ASCII')

    # Replaces invalid characters with _
    safe = re.sub(r'[^\w\-_.]', '_', ascii_text)

    # Remove multyples underscores
    safe = re.sub(r'_+', '_', safe)

    # Remove underscores no start/end
    safe = safe.strip('_')

    # Limits size
    if len(safe) > max_length:
        safe = safe[:max_length]

    return safe


def open_about():
    about_window = tb.Toplevel(mainwindow)
    about_window.title(LANG[current_lang]["about"])
    about_window.geometry("420x220")
    about_window.resizable(False, False)
    about_window.iconbitmap("icon.ico")

    text = tk.Text(about_window, wrap="word", padx=25, pady=25, font=("IBM Plex Sans", 10), width=50, height=8)
    text.insert("1.0", LANG[current_lang]["about_text"])
    text.config(state="disabled")
    text.pack(expand=True, fill="both")


def open_github():
    webbrowser.open("https://github.com/alexbccastro/OSM2Syntax")


def open_tutorial():
    tutorial_window = tb.Toplevel(mainwindow)
    tutorial_window.title(LANG[current_lang]["quick_tutorial"])
    tutorial_window.geometry("695x350")
    tutorial_window.resizable(False, False)
    tutorial_window.iconbitmap("icon.ico")

    text = tk.Text(tutorial_window, wrap="word", padx=20, pady=20, font=("IBM Plex Sans", 10), width=85, )
    text.insert("1.0", LANG[current_lang]["tutorial_text"])
    text.config(state="disabled")
    text.pack(expand=True, fill="both")


def preview_data():
    threading.Thread(target=run_preview, daemon=True).start()


def run_download():
    cancel_event.clear()

    try:
        start_time = time.time()
        mainwindow.after(0, lambda: start_progress(LANG[current_lang]["status_connecting"]))

        custom_filter = ('["highway"~"motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary|'
                         'secondary_link|tertiary|tertiary_link|residential|living_street|unclassified|road|'
                         'pedestrian"]')

        simplify_flag = simplify_checkbutton_var.get()
        preview_button.config(state="disabled", cursor="arrow")

        # Define Place
        if name_checkbutton_var.get():
            place = name_entry.get().strip()
            if not place:
                raise ValueError(LANG[current_lang]["empty_name"])

            location_info = place

            g = ox.graph_from_place(place, custom_filter=custom_filter, simplify=simplify_flag)
            check_cancel()

            safe_place = make_safe_filename(place)
            filename_base = f"rcl_{safe_place}"

        else:
            lat = float(lat_entry_var.get())
            lon = float(long_entry_var.get())
            radius = float(radius_entry_var.get())

            location_info = f"Lat: {lat}, Lon: {lon}, Radius: {radius}m"

            g = ox.graph_from_point((lat, lon), dist=radius, custom_filter=custom_filter,
                                    simplify=simplify_flag)
            check_cancel()

            coord_part = f"{lat:.5f}_{lon:.5f}".replace("-", "").replace(".", "p")
            filename_base = make_safe_filename(f"rcl_{coord_part}_r{int(radius)}")

        # -------------------------
        mainwindow.after(0, lambda: set_progress(30, LANG[current_lang]["status_processing"]))

        g = g.to_undirected()
        check_cancel()

        largest_cc = max(nx.connected_components(g), key=len)
        g = g.subgraph(largest_cc).copy()
        check_cancel()

        g_proj = ox.project_graph(g)
        nodes, edges = ox.graph_to_gdfs(g_proj)
        check_cancel()

        # Metrics Before
        total_vertices_before = edges.geometry.apply(lambda g: len(g.coords)).sum()
        total_length_before = edges.length.sum()

        # RCL Simplification
        mainwindow.after(0, lambda: set_progress(50, LANG[current_lang]["status_simplifying"]))

        if simplify_flag:

            angle_threshold = float(angle_threshold_var.get())
            tolerance = float(tolerance_var.get())

            def calculate_angle(a, b, c):
                ba = np.array(a) - np.array(b)
                bc = np.array(c) - np.array(b)
                cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
                return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

            def simplify_line(line):
                coords = list(line.coords)
                if len(coords) <= 2:
                    return line

                preserved = [coords[0]]
                for i in range(1, len(coords) - 1):

                    if cancel_event.is_set():
                        raise RuntimeError(LANG[current_lang]["cancelled"])

                    angle = calculate_angle(coords[i - 1], coords[i], coords[i + 1])
                    if angle > angle_threshold:
                        preserved.append(coords[i])

                preserved.append(coords[-1])
                return LineString(preserved).simplify(tolerance, preserve_topology=False)

            edges["geometry"] = edges.geometry.apply(simplify_line)
            check_cancel()

            total_vertices_after = edges.geometry.apply(lambda g: len(g.coords)).sum()
            total_length_after = edges.length.sum()

            vertex_reduction = ((total_vertices_before - total_vertices_after) /
                                total_vertices_before * 100)

            length_variation = ((total_length_after - total_length_before) /
                                total_length_before * 100)

            filename_base += f"_AT{int(angle_threshold)}_TO{int(tolerance)}"

        else:
            angle_threshold = "-"
            tolerance = "-"
            total_vertices_after = total_vertices_before
            total_length_after = total_length_before
            vertex_reduction = 0
            length_variation = 0
            filename_base += "_original"

        # -------------------------
        mainwindow.after(0, lambda: set_progress(75, LANG[current_lang]["status_saving"]))

        folder = saveas_entry_var.get()
        base_path = os.path.join(folder, filename_base)
        filepath_network = base_path + ".gpkg"

        counter = 1
        while os.path.exists(filepath_network):
            filepath_network = f"{base_path}_v{counter}.gpkg"
            counter += 1

        edges.to_file(filepath_network, layer="edges", driver="GPKG")
        check_cancel()

        nodes.to_file(filepath_network, layer="nodes", driver="GPKG")
        check_cancel()

        # Background Leyers Download
        background_files = []

        if buildings_var.get():

            buildings_tags = {"building": True}

            if name_checkbutton_var.get():
                gdf_buildings = ox.features_from_place(place, buildings_tags)
            else:
                gdf_buildings = ox.features_from_point((lat, lon), buildings_tags, dist=radius)

            if not gdf_buildings.empty:
                buildings_path = base_path + "_buildings.gpkg"
                gdf_buildings.to_file(buildings_path, driver="GPKG")
                background_files.append("Buildings")

        check_cancel()

        if nature_var.get():

            vegetation_tags = {"natural": True}

            if name_checkbutton_var.get():
                gdf_veg = ox.features_from_place(place, vegetation_tags)
            else:
                gdf_veg = ox.features_from_point((lat, lon), vegetation_tags, dist=radius)

            if not gdf_veg.empty:
                veg_path = base_path + "_vegetation.gpkg"
                gdf_veg.to_file(veg_path, driver="GPKG")
                background_files.append("Vegetation")

        check_cancel()

        if park_var.get():

            park_tags = {"leisure": ["park", "dog_park"]}

            if name_checkbutton_var.get():
                gdf_park = ox.features_from_place(place, park_tags)
            else:
                gdf_park = ox.features_from_point((lat, lon), park_tags, dist=radius)

            if not gdf_park.empty:
                park_path = base_path + "_park.gpkg"
                gdf_park.to_file(park_path, driver="GPKG")
                background_files.append("Park")

        check_cancel()

        if water_var.get():

            water_tags = {"natural": ["water"], "waterway": True}

            if name_checkbutton_var.get():
                gdf_water = ox.features_from_place(place, water_tags)
            else:
                gdf_water = ox.features_from_point((lat, lon), water_tags, dist=radius)

            if not gdf_water.empty:
                water_path = base_path + "_water.gpkg"
                gdf_water.to_file(water_path, driver="GPKG")
                background_files.append("Water")

        check_cancel()

        # Report Generation
        file_size_mb = os.path.getsize(filepath_network) / (1024 * 1024)
        end_time = time.time()
        download_time = end_time - start_time

        report_path = base_path + "_report.txt"

        lang = LANG[current_lang]

        report_text = f"""
        {lang["report_title"]}
        ============================

        {lang["date"]}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        {lang["location"]}: {location_info}
        {lang["network_type"]}: {lang["simplified"] if simplify_flag else lang["original"]}

        {lang["file"]}: {os.path.basename(filepath_network)}
        {lang["file_size"]}: {file_size_mb:.2f} MB
        {lang["download_time"]}: {download_time:.2f} {lang["seconds"]}

        {lang["background_layers"]}:
        {', '.join(background_files) if background_files else lang["none"]}

        {lang["metrics"]}
        -----------------------

        {lang["angle_threshold"]}: {angle_threshold}
        {lang["tolerance"]}: {tolerance}

        {lang["vertices_before"]}: {int(total_vertices_before)}
        {lang["vertices_after"]}: {int(total_vertices_after)}
        {lang["vertex_reduction"]}: {vertex_reduction:.2f}

        {lang["length_before"]}: {total_length_before:.2f}
        {lang["length_after"]}: {total_length_after:.2f}
        {lang["length_variation"]}: {length_variation:.2f}
        """

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        lang = LANG[current_lang]

        mainwindow.after(0, lambda: finish_progress())
        mainwindow.after(0, lambda: messagebox.showinfo(LANG[current_lang]["download_completed_title"],
                                                        f"{LANG[current_lang]['download_completed']}\n\n"
                                                        f"{LANG[current_lang]['download_time']}: {download_time:.2f} {lang['seconds']}\n\n"))

    except RuntimeError as e:
        if str(e) == LANG[current_lang]["cancelled"]:
            mainwindow.after(0, lambda: error_progress(LANG[current_lang]["download_cancelled"]))
            return

    except Exception as e:
        error_message = str(e)
        mainwindow.after(0, lambda: error_progress(error_message))
        mainwindow.after(0, lambda: messagebox.showerror(LANG[current_lang]["empty_name"], error_message))


def run_preview():
    global preview_state
    try:
        preview_state = "loading"
        mainwindow.after(0, lambda: preview_status.config(
            text=LANG[current_lang]["preview_loading"]
        ))

        g = build_graph_preview()

        mainwindow.after(0, lambda: update_plot(g))

        preview_state = "loaded"
        mainwindow.after(0, lambda: preview_status.config(
            text=LANG[current_lang]["preview_loaded"]
        ))
        mainwindow.after(0, lambda: save_preview_button.config(state="normal", cursor="hand2"))
        mainwindow.after(0, lambda: preview_button.config(state="normal", cursor="hand2"))

    except Exception as e:
        preview_state = "none"
        mainwindow.after(0, lambda: messagebox.showerror(
            LANG[current_lang]["preview_error"], str(e)
        ))
        mainwindow.after(0, lambda: preview_status.config(
            text=LANG[current_lang]["preview_none"]
        ))
        mainwindow.after(0, lambda: preview_button.config(state="normal", cursor="hand2"))


def save_preview():
    try:
        filetypes = [("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("PDF File", "*.pdf")]

        default_name = f"preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        filepath = filedialog.asksaveasfilename(initialfile=default_name, defaultextension=".png", filetypes=filetypes,
                                                title=LANG[current_lang]["save_preview_as"])

        if not filepath:
            return

        # Rebuild Graph Preview
        g = build_graph_preview()

        # Create Temporary Image
        fig_export, ax_export = plt.subplots(figsize=(5, 5.7), dpi=300)

        fig_export.patch.set_facecolor("white")
        ax_export.set_facecolor("white")

        ox.plot_graph(g, ax=ax_export, show=False, close=False, node_size=0, edge_color="black", edge_linewidth=0.4,
                      edge_alpha=0.7, bgcolor="white")

        ax_export.set_axis_off()
        fig_export.subplots_adjust(left=0, right=1, top=1, bottom=0)
        fig_export.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close(fig_export)

        messagebox.showinfo(LANG[current_lang]["preview_saved_title"], LANG[current_lang]["preview_saved_message"])

    except Exception as e:
        messagebox.showerror(LANG[current_lang]["error_title"], str(e))


def set_dark_entry_style():
    style.configure("Modern.TEntry", fieldbackground="#1c1c1c", foreground="#f8f9fa", bordercolor="#bfbfbf",
                    insertcolor="#4dabf7")

    style.map("Modern.TEntry", fieldbackground=[("disabled", "#3e444a"), ("readonly", "#343a40"), ("focus",
                                                                                                   "#1c1c1c")],
              foreground=[("disabled", "#868e96")], bordercolor=[("focus", "#4dabf7")])


def set_language(lang):
    global current_lang
    current_lang = lang
    update_menu_language()

    download_button.config(text=LANG[lang]["download"])
    cancel_button.config(text=LANG[lang]["cancel"])
    clean_button.config(text=LANG[lang]["clear"])
    preview_button.config(text=LANG[lang]["preview"])
    save_preview_button.config(text=LANG[lang]["plot"])
    name_checkbutton.config(text=LANG[lang]["name"])
    point_checkbutton.config(text=LANG[lang]["point"])
    radius_label.config(text=LANG[lang]["radius"])
    simplify_checkbutton.config(text=LANG[lang]["simplify"])
    angle_threshold_label.config(text=LANG[lang]["angular_threshold"])
    tolerance_label.config(text=LANG[lang]["tolerance"])
    background_label.config(text=LANG[lang]["background_layers"])
    buildings_checkbutton.config(text=LANG[lang]["buildings"])
    nature_checkbutton.config(text=LANG[lang]["nature"])
    park_checkbutton.config(text=LANG[lang]["park"])
    water_checkbutton.config(text=LANG[lang]["water"])
    saveas_label.config(text=LANG[lang]["saveas"])
    if preview_state == "none":
        preview_status.config(text=LANG[lang]["preview_none"])
    elif preview_state == "loading":
        preview_status.config(text=LANG[lang]["preview_loading"])
    elif preview_state == "loaded":
        preview_status.config(text=LANG[lang]["preview_loaded"])
    menubar.entryconfig(0, label=LANG[lang]["menu"])
    menubar.entryconfig(1, label=LANG[lang]["view"])
    menubar.entryconfig(2, label=LANG[lang]["help"])
    file_menu.entryconfig(0, label=LANG[lang]["clear"])
    file_menu.entryconfig(2, label=LANG[lang]["exit"])
    view_menu.entryconfig(0, label=LANG[lang]["dark_mode"])
    view_menu.entryconfig(1, label=LANG[lang]["fullscreen"])
    help_menu.entryconfig(0, label=LANG[lang]["about"])
    help_menu.entryconfig(1, label=LANG[lang]["github"])
    help_menu.entryconfig(3, label=LANG[lang]["quick_tutorial"])
    tooltip_name.text = LANG[lang]["tooltip_name"]
    tooltip_point.text = LANG[lang]["tooltip_point"]
    tooltip_radius.text = LANG[lang]["tooltip_radius"]
    tooltip_simplify.text = LANG[lang]["tooltip_simplify"]
    tooltip_angle.text = LANG[lang]["tooltip_angle"]
    tooltip_tolerance.text = LANG[lang]["tooltip_tolerance"]

    if progress_bar_var.get() == 0:
        status_txt.config(text=LANG[lang]["status_waiting"])

    if dark_mode_var.get():
        darktheme_button.config(text=LANG[lang]["btn_light"])
    else:
        darktheme_button.config(text=LANG[lang]["btn_dark"])

    status_txt.config(
        text=f"{LANG[lang]['status_prefix']}{LANG[lang]['download_completed']}"
    )

def set_light_entry_style():
    # Light mode entry
    style.configure("Modern.TEntry", fieldbackground="#FFFFFF", foreground="#212529", bordercolor="#CED4DA",
                    lightcolor="#CED4DA", darkcolor="#CED4DA")

    # States
    style.map("Modern.TEntry", fieldbackground=[("disabled", "#E9ECEF"), ("readonly", "#F8F9FA")],
              foreground=[("disabled", "#6C757D")], bordercolor=[("focus", "#86B7FE")])


def set_progress(value, message=None):
    progress_bar.stop()
    progress_bar.config(mode="determinate")
    progress_bar_var.set(value)
    if message:
        status_txt.config(text=message)


def start_progress(message="Working..."):
    cancel_event.clear()
    global progress_state, cancel_download_flag
    cancel_download_flag = False

    progress_state = "primary"
    progress_bar.config(mode="indeterminate", bootstyle="primary")
    progress_bar.start(10)

    status_txt.config(text=f"{LANG[current_lang]['status_prefix']}{message}")

    download_button.config(state="disabled", cursor="arrow")
    clean_button.config(state="disabled", cursor="arrow")
    preview_button.config(state="disabled", cursor="arrow")
    save_preview_button.config(state="disabled", cursor="arrow")
    darktheme_button.config(state="disabled", cursor="arrow")
    cancel_button.config(state="normal", cursor="hand2")


def toggle_dark_mode():
    if style.theme_use() == "flatly":
        # Activate Dark Mode
        style.theme_use("darkly")
        dark_mode_var.set(True)
        set_dark_entry_style()

        darktheme_button.configure(text=LANG[current_lang]["btn_light"], image=moon_icon, bootstyle="light")
        btn_en.config(bootstyle='dark')
        btn_pt.config(bootstyle='dark')
    else:
        # Activate Light Mode
        style.theme_use("flatly")
        dark_mode_var.set(False)
        set_light_entry_style()

        darktheme_button.configure(text=LANG[current_lang]["btn_dark"], image=sun_icon, bootstyle="primary")
        btn_en.config(bootstyle='light')
        btn_pt.config(bootstyle='light')

    update_logo()
    apply_global_font()
    update_button_styles()

    # Update Graph Background
    if dark_mode_var.get():
        fig.patch.set_facecolor("#222222")
        ax.set_facecolor("#222222")
    else:
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

    canvas.draw()

    if len(fig.axes) > 0:
        try:
            g = build_graph()
            update_plot(g)
        except:
            pass


def toggle_fullscreen():
    state = not mainwindow.attributes("-fullscreen")
    mainwindow.attributes("-fullscreen", state)
    fullscreen_var.set(state)


def toggle_name():
    if name_checkbutton_var.get():
        name_entry.config(state="normal")
        point_checkbutton_var.set(False)
        toggle_point()
    else:
        name_entry.delete(0, tk.END)
        name_entry.config(state="disabled")
    check_download_ready()
    update_preview_button_state()


def toggle_point():
    if point_checkbutton_var.get():
        lat_entry.config(state="normal")
        long_entry.config(state="normal")
        radius_entry.config(state="normal")
        name_checkbutton_var.set(False)
        toggle_name()
    else:
        lat_entry_var.set("")
        long_entry_var.set("")
        radius_entry_var.set("")
        lat_entry.config(state="disabled")
        long_entry.config(state="disabled")
        radius_entry.config(state="disabled")
    check_download_ready()
    update_preview_button_state()


def toggle_simplify():
    if simplify_checkbutton_var.get():
        angle_threshold_entry.config(state="normal")
        tolerance_entry.config(state="normal")
    else:
        angle_threshold_entry.config(state="disabled")
        tolerance_entry.config(state="disabled")


def update_button_styles():
    saveas_button.configure(bootstyle="info")
    clean_button.configure(bootstyle="warning")
    download_button.configure(bootstyle="primary")
    progress_bar.configure(bootstyle=progress_state)


def update_menu_language():
    lang = LANG[current_lang]

    menubar.entryconfig(0, label=lang["menu"])
    menubar.entryconfig(1, label=lang["view"])
    menubar.entryconfig(2, label=lang["help"])

    file_menu.entryconfig(0, label=lang["clear"])
    file_menu.entryconfig(2, label=lang["exit"])

    view_menu.entryconfig(0, label=lang["dark_mode"])
    view_menu.entryconfig(1, label=lang["fullscreen"])

    help_menu.entryconfig(0, label=lang["about"])
    help_menu.entryconfig(1, label=lang["github"])
    help_menu.entryconfig(3, label=lang["quick_tutorial"])


def update_logo():
    current_theme = style.theme_use()

    if current_theme == "darkly":
        logo_label.configure(image=logo_dark)
        logo_label.image = logo_dark
    else:
        logo_label.configure(image=logo_light)
        logo_label.image = logo_light


def update_plot(g):
    fig.clear()

    dark = dark_mode_var.get()

    if dark:
        bgcolor = "#222222"
        edge_color = "white"
    else:
        bgcolor = "white"
        edge_color = "black"

    fig.patch.set_facecolor(bgcolor)

    ax = fig.add_subplot(111)
    ax.set_facecolor(bgcolor)

    ox.plot_graph(g, ax=ax, show=False, close=False, node_size=0, edge_color=edge_color, edge_linewidth=0.4,
                  edge_alpha=0.7, bgcolor=bgcolor)

    ax.set_aspect("equal", adjustable="box")
    ax.set_axis_off()
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    canvas.draw()


def update_preview_button_state():
    if name_checkbutton_var.get():

        if name_entry_var.get().strip():
            preview_button.config(state="normal", cursor="hand2")
        else:
            preview_button.config(state="disabled", cursor="arrow")

    elif point_checkbutton_var.get():

        lat = lat_entry_var.get().strip()
        lon = long_entry_var.get().strip()
        radius = radius_entry_var.get().strip()

        try:
            lat = float(lat)
            lon = float(lon)
            radius = float(radius)

            if -90 <= lat <= 90 and -180 <= lon <= 180 and radius > 0:
                preview_button.config(state="normal", cursor="hand2")
            else:
                preview_button.config(state="disabled", cursor="arrow")

        except ValueError:
            preview_button.config(state="disabled", cursor="arrow")

    else:
        preview_button.config(state="disabled", cursor="arrow")


# Tooltip
class ToolTip:

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):

        if self.tipwindow or not self.text:
            return

        x = self.widget.winfo_rootx() + 15
        y = self.widget.winfo_rooty() + 20

        self.tipwindow = tw = tk.Toplevel(self.widget)

        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            font=("IBM Plex Sans", 9),
            justify="left",
            relief="solid",
            borderwidth=1
        )

        label.pack(ipadx=6, ipady=3)

    def hide(self, event=None):

        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


############################################# Graphic User Interface (GUI)#############################################
# Main window
mainwindow = tb.Window(themename="flatly")
mainwindow.title("OSM2Syntax, v. 1.0.2")
mainwindow.resizable(False, False)
mainwindow.iconbitmap("icon.ico")

# Main Layout (Left + Right)
main_container = tb.Frame(mainwindow)
main_container.pack(fill="both", expand=True)
main_container.columnconfigure(0, weight=3)
main_container.columnconfigure(1, weight=0)  # separator
main_container.columnconfigure(2, weight=1)
main_container.rowconfigure(0, weight=1)

left_panel = tb.Frame(main_container)
left_panel.grid(row=0, column=0, sticky="nsew")
left_panel.columnconfigure(0, weight=3)

separator = tb.Frame(main_container, width=2)
separator.configure(style="secondary.TFrame")
separator.grid(row=0, column=1, pady=30, sticky="ns")

right_panel = tb.Frame(main_container)
right_panel.grid(row=0, column=2, sticky="nsew")
right_panel.columnconfigure(0, weight=1)

# Upper Menu
menubar = tb.Menu(mainwindow)
file_menu = tb.Menu(menubar, tearoff=0)
help_menu = tb.Menu(menubar, tearoff=0)
view_menu = tb.Menu(menubar, tearoff=0)
mainwindow.config(menu=menubar)

# File Menu
file_menu.add_command(label=LANG[current_lang]["clear"], command=clear_all, accelerator="Ctrl+L")
file_menu.add_separator()
file_menu.add_command(label=LANG[current_lang]["exit"], command=mainwindow.quit, accelerator="Ctrl+Q")
menubar.add_cascade(label=LANG[current_lang]["menu"], menu=file_menu)

# View Menu
view_menu.add_command(label=LANG[current_lang]["dark"], command=toggle_dark_mode, accelerator="Ctrl+D")
view_menu.add_command(label=LANG[current_lang]["fullscreen"], command=toggle_fullscreen, accelerator="F11")
menubar.add_cascade(label=LANG[current_lang]["view"], menu=view_menu)

# Help Menu
help_menu.add_command(label=LANG[current_lang]["about"], command=open_about)
help_menu.add_command(label=LANG[current_lang]["github"], command=open_github)
help_menu.add_separator()
help_menu.add_command(label=LANG[current_lang]["quick_tutorial"], command=open_tutorial)
menubar.add_cascade(label=LANG[current_lang]["help"], menu=help_menu)

fullscreen_var = tk.BooleanVar()

mainwindow.bind("<Control-l>", lambda event: clear_all())
mainwindow.bind("<Control-q>", lambda event: mainwindow.quit())
mainwindow.bind("<Control-d>", lambda event: toggle_dark_mode())
mainwindow.bind("<F11>", lambda e: mainwindow.attributes("-fullscreen", True))
mainwindow.bind("<Escape>", lambda e: mainwindow.attributes("-fullscreen", False))
mainwindow.bind("<F11>", lambda event: toggle_fullscreen())
mainwindow.bind("<Escape>", exit_fullscreen)

# Style Configuration
load_custom_font()
style = mainwindow.style
style.configure(".", font=("IBM Plex Sans Medium", 10))
style.configure("Modern.TEntry", fieldbackground="#FFFFFF", bordercolor="#CED4DA", lightcolor="#CED4DA",
                darkcolor="#CED4DA")
style.map("Modern.TEntry", fieldbackground=[("disabled", "#E9ECEF")], foreground=[("disabled", "#6C757D")])

# Dark Mode Variables
dark_mode_var = tk.BooleanVar(value=False)

# Images
clear_img = Image.open("icon_clear.png").resize((18, 18))
clear_icon = ImageTk.PhotoImage(clear_img)
download_img = Image.open("icon_download.png").resize((18, 18))
download_icon = ImageTk.PhotoImage(download_img)
sun_img = Image.open("icon_sun.png").resize((20, 20))
sun_icon = ImageTk.PhotoImage(sun_img)
moon_img = Image.open("icon_moon.png").resize((20, 20))
moon_icon = ImageTk.PhotoImage(moon_img)
preview_img = Image.open("icon_preview.png").resize((22, 22))
preview_icon = ImageTk.PhotoImage(preview_img)
save_preview_img = Image.open("icon_savepreview.png").resize((22, 22))
save_preview_icon = ImageTk.PhotoImage(save_preview_img)
cancel_img = Image.open("icon_cancel.png").resize((18, 18))
cancel_icon = ImageTk.PhotoImage(cancel_img)
flag_br_img = Image.open("icon_br.png").resize((18, 18))
flag_br_icon = ImageTk.PhotoImage(flag_br_img)
flag_uk_img = Image.open("icon_uk.png").resize((18, 18))
flag_uk_icon = ImageTk.PhotoImage(flag_uk_img)
logo_light_img = Image.open("logo_txt_black.png")
logo_light = ImageTk.PhotoImage(logo_light_img)
logo_dark_img = Image.open("logo_txt_white.png")
logo_dark = ImageTk.PhotoImage(logo_dark_img)

# Header frame
header_frame = tb.Frame(left_panel)
header_frame.grid(row=0, column=0, sticky="ew")
logo_label = tb.Label(header_frame, image=logo_light)
logo_label.pack(pady=5)
tb.Separator(left_panel, orient="horizontal").grid(row=1, column=0, sticky="ew")

############################################### LEFT PANEL ###########################################################

# Left Panel Widgets Frames
name_checkbutton_frame = tb.Frame(left_panel)
name_checkbutton_frame.grid(row=1, column=0, sticky="ew")
name_checkbutton_frame.rowconfigure(0, weight=1)
name_checkbutton_frame.columnconfigure(0, weight=1)

name_entry_frame = tb.Frame(left_panel)
name_entry_frame.grid(row=2, column=0, sticky="ew")
name_entry_frame.columnconfigure(0, weight=1)

point_checkbutton_frame = tb.Frame(left_panel)
point_checkbutton_frame.grid(row=3, column=0, sticky="ew")
point_checkbutton_frame.columnconfigure(0, weight=1)
point_checkbutton_frame.rowconfigure(0, weight=1)
point_checkbutton_frame.columnconfigure(0, weight=1)

latlong_frame = tb.Frame(left_panel)
latlong_frame.grid(row=4, column=0, sticky="ew")
latlong_frame.rowconfigure(0, weight=1)
latlong_frame.rowconfigure(1, weight=1)
latlong_frame.columnconfigure(0, weight=1)

simplify_checkbutton_frame = tb.Frame(left_panel)
simplify_checkbutton_frame.grid(row=5, column=0, sticky="ew")
simplify_checkbutton_frame.columnconfigure(0, weight=1)
simplify_checkbutton_frame.rowconfigure(0, weight=1)

simplify_frame = tb.Frame(left_panel)
simplify_frame.grid(row=6, column=0, sticky="ew")
simplify_frame.rowconfigure(0, weight=1)
simplify_frame.columnconfigure(0, weight=1)

background_label_frame = tb.Frame(left_panel)
background_label_frame.grid(row=7, column=0, sticky="ew")
background_label_frame.rowconfigure(0, weight=1)

background_frame = tb.Frame(left_panel)
background_frame.grid(row=8, column=0, sticky="ew")
background_frame.rowconfigure(0, weight=1)
background_frame.columnconfigure(0, weight=1)
background_frame.columnconfigure(1, weight=1)
background_frame.columnconfigure(2, weight=1)
background_frame.columnconfigure(3, weight=1)

saveas_label_frame = tb.Frame(left_panel)
saveas_label_frame.grid(row=9, column=0, sticky="ew")
saveas_frame = tb.Frame(left_panel)
saveas_frame.grid(row=10, column=0, sticky="ew")
saveas_frame.rowconfigure(0, weight=1)
saveas_frame.columnconfigure(0, weight=1)
saveas_frame.columnconfigure(1, weight=25)

download_frame = tb.Frame(left_panel)
download_frame.grid(row=11, column=0, sticky="ew")
download_frame.rowconfigure(0, weight=1)
download_frame.columnconfigure(0, weight=1)
download_frame.columnconfigure(1, weight=1)
download_frame.columnconfigure(2, weight=1)

status_frame = tb.Frame(left_panel)
status_frame.grid(row=12, column=0, sticky="ew")
status_frame.rowconfigure(0, weight=1)
status_frame.columnconfigure(0, weight=1)

# Left Panel Widgets
# Name Checkbutton
name_checkbutton_var = tk.BooleanVar()
name_checkbutton = tb.Checkbutton(name_checkbutton_frame, text='Name (OSM Nomitatim)', variable=name_checkbutton_var,
                                  command=toggle_name, bootstyle="info-round-toggle", cursor="hand2")
name_checkbutton.grid(row=0, column=0, padx=20, pady=(0, 10), sticky='ew')
tooltip_name = ToolTip(name_checkbutton, LANG[current_lang]["tooltip_name"])

# Dark Mode Button
darktheme_button = tb.Button(name_checkbutton_frame, text='Dark Mode', command=toggle_dark_mode, image=sun_icon,
                             bootstyle="primary", compound="left", cursor="hand2", width=10)
darktheme_button.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

# Name Entry
name_entry_var = tk.StringVar()
name_entry_var.trace_add("write", lambda *args: update_preview_button_state())
name_entry = tb.Entry(name_entry_frame, width=30, state='disabled', style="Modern.TEntry", textvariable=name_entry_var)
name_entry.grid(row=0, column=0, padx=20, pady=(0, 20), columnspan=6, sticky='ew')

# Point Checkbutton
point_checkbutton_var = tk.BooleanVar()
point_checkbutton = tb.Checkbutton(point_checkbutton_frame, text='Point (Decimal Degrees)',
                                   variable=point_checkbutton_var, command=toggle_point, cursor="hand2",
                                   bootstyle="info-round-toggle")
point_checkbutton.grid(row=0, column=0, padx=20, pady=(0, 10), sticky='ew')
tooltip_point = ToolTip(point_checkbutton, LANG[current_lang]["tooltip_point"])

# Lat Long Label
lat_label = tb.Label(latlong_frame, text='Latitude:', foreground='#808080', justify='left', anchor='w')
lat_label.grid(row=0, column=0, padx=20, pady=(0, 3), sticky='ew')

# Lat Entry
lat_entry_var = tk.StringVar()
lat_entry_var.trace_add("write", lambda *args: update_preview_button_state())
lat_entry = tb.Entry(latlong_frame, textvariable=lat_entry_var, state='disabled', style="Modern.TEntry", width=10)
lat_entry.grid(row=1, column=0, padx=20, pady=(0, 5), sticky='ew')

# long Label
long_label = tb.Label(latlong_frame, text='Longitude:', foreground='#808080', justify='left', anchor='w')
long_label.grid(row=2, column=0, padx=20, pady=(0, 3), sticky='ew')

# Long Entry
long_entry_var = tk.StringVar()
long_entry_var.trace_add("write", lambda *args: update_preview_button_state())
long_entry = tb.Entry(latlong_frame, textvariable=long_entry_var, state='disabled', style="Modern.TEntry", width=10)
long_entry.grid(row=3, column=0, padx=20, pady=(0, 5), sticky='ew')

# Radius Label
radius_label = tb.Label(latlong_frame, text='Radius (m):', foreground='#808080', justify='left', anchor='w')
radius_label.grid(row=4, column=0, padx=20, pady=(0, 3), sticky='ew')
tooltip_radius = ToolTip(radius_label, LANG[current_lang]["tooltip_radius"])

# Radius Entry
radius_entry_var = tk.StringVar()
radius_entry_var.trace_add("write", lambda *args: update_preview_button_state())
radius_entry = tb.Entry(latlong_frame, textvariable=radius_entry_var, state='disabled', style="Modern.TEntry", width=10)
radius_entry.grid(row=5, column=0, padx=20, pady=(0, 20), sticky='ew')

# Simplify Checkbutton
simplify_checkbutton_var = tk.BooleanVar()
simplify_checkbutton = tb.Checkbutton(simplify_checkbutton_frame, text="Simplify RCL",
                                      variable=simplify_checkbutton_var, command=toggle_simplify, cursor="hand2",
                                      bootstyle="info-round-toggle")
simplify_checkbutton.grid(row=0, column=0, padx=20, pady=(0, 10), sticky='ew')
tooltip_simplify = ToolTip(simplify_checkbutton, LANG[current_lang]["tooltip_simplify"])

# Angle Threshold Label
angle_threshold_var = tk.IntVar(value=5)
angle_threshold_label = tb.Label(simplify_frame, text='Angle Threshold:', foreground='#808080', anchor='w')
angle_threshold_label.grid(row=0, column=0, padx=20, pady=(0, 3), sticky='ew')
tooltip_angle = ToolTip(angle_threshold_label, LANG[current_lang]["tooltip_angle"])

# Angle Threshold Entry
angle_threshold_entry = tb.Entry(simplify_frame, textvariable=angle_threshold_var, state='disabled',
                                 style="Modern.TEntry", width=10)
angle_threshold_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 5), sticky='ew')

# Tolerance Label
tolerance_var = tk.IntVar(value=10)
tolerance_label = tb.Label(simplify_frame, text='Tolerance:', foreground='#808080', anchor='w')
tolerance_label.grid(row=2, column=0, padx=20, pady=(0, 3), sticky='ew')
tooltip_tolerance = ToolTip(tolerance_label, LANG[current_lang]["tooltip_tolerance"])

# Tolerance Entry
tolerance_entry = tb.Entry(simplify_frame, textvariable=tolerance_var, state='disabled', style="Modern.TEntry",
                           width=10)
tolerance_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 20), sticky='ew')

# Background Label
background_label = tb.Label(background_label_frame, text='Background Layers', anchor='w')
background_label.grid(row=0, column=0, padx=20, pady=(0, 5), sticky='ew')

# Buildings Checkbutton
buildings_var = tk.BooleanVar()
buildings_checkbutton = tb.Checkbutton(background_frame, text='Buildings', variable=buildings_var, cursor="hand2",
                                       bootstyle="info-round-toggle")
buildings_checkbutton.grid(row=0, column=0, padx=20, pady=(0, 20), sticky='ew')

# Nature Checkbutton
nature_var = tk.BooleanVar()
nature_checkbutton = tb.Checkbutton(background_frame, text='Nature', variable=nature_var, cursor="hand2",
                                    bootstyle="info-round-toggle")
nature_checkbutton.grid(row=0, column=1, padx=(0, 20), pady=(0, 20), sticky='ew')

# Park Checkbutton
park_var = tk.BooleanVar()
park_checkbutton = tb.Checkbutton(background_frame, text='Park', bootstyle="info-round-toggle", variable=park_var,
                                  cursor="hand2")
park_checkbutton.grid(row=0, column=2, padx=(0, 20), pady=(0, 20), sticky='ew')

# Water Checkbutton
water_var = tk.BooleanVar()
water_checkbutton = tb.Checkbutton(background_frame, text='Water', bootstyle="info-round-toggle", variable=water_var,
                                   cursor="hand2")
water_checkbutton.grid(row=0, column=3, padx=(0, 20), pady=(0, 20), sticky='ew')

# Save As Label
saveas_label = tb.Label(saveas_label_frame, text='Folder to Save the Data')
saveas_label.grid(row=0, column=0, padx=20, pady=(0, 5), sticky='ew')

# Save As Button
saveas_button = tb.Button(saveas_frame, text='...', width=2, command=choose_directory, bootstyle="info",
                          compound="left", cursor="hand2")

saveas_button.grid(row=0, column=0, padx=(20, 10), pady=(0, 10), sticky='w')

# Save As Entry
saveas_entry_var = tk.StringVar()
saveas_entry = tb.Entry(saveas_frame, textvariable=saveas_entry_var, width=30, style="Modern.TEntry")
saveas_entry.grid(row=0, column=1, padx=(0, 20), pady=(0, 10), sticky='ew')

# Download Button
download_button = tb.Button(download_frame, text='Download', command=download_data, bootstyle="primary",
                            image=download_icon, compound="left", state="disabled", width=10)
download_button.grid(row=0, column=0, padx=20, pady=(0, 20))

# Cancel Button
cancel_button = tb.Button(download_frame, text='Cancel', command=cancel_download, bootstyle="danger",
                          state="disabled", image=cancel_icon, compound='left', width=10)
cancel_button.grid(row=0, column=1, padx=(0, 20), pady=(0, 20))

# Clean Button
clean_button = tb.Button(download_frame, text='Clear', command=clear_all, bootstyle="warning", image=clear_icon,
                         compound="left", width=10, cursor="hand2")
clean_button.grid(row=0, column=2, padx=(0, 20), pady=(0, 20))

# progress bar
progress_bar_var = tk.DoubleVar()
progress_bar = tb.Progressbar(download_frame, variable=progress_bar_var, bootstyle="primary", mode="determinate")
progress_bar.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 3), sticky="ew")
progress_state = "primary"

# status label
status_txt = tb.Label(status_frame, text="Status: Waiting")
status_txt.grid(row=0, column=0, columnspan=8, padx=20, pady=(0, 20))

############################################### RIGHT PANEL ###########################################################

# Right Panel Frames
preview_top_frame = tb.Frame(right_panel)
preview_top_frame.grid(row=0, column=0, pady=(20, 10))

preview_frame = tb.Frame(right_panel)
preview_frame.grid(row=1, column=0, padx=20, pady=10, sticky="n")

lang_frame = tb.Frame(right_panel)
lang_frame.grid(row=2, column=0, padx=10, pady=10, sticky='e')

# Right Panel Widgets
# Preview Button
preview_button = tb.Button(preview_top_frame, text="Preview", command=preview_data, bootstyle="info",
                           image=preview_icon, compound="left", state="disabled", width=10)
preview_button.grid(row=0, column=0, padx=(0, 20), pady=(10, 0))

# Plot Preview
save_preview_button = tb.Button(preview_top_frame, text="Plot", command=save_preview, image=save_preview_icon,
                                compound="left", bootstyle="primary", state="disabled", width=10)
save_preview_button.grid(row=0, column=1, pady=(10, 0))

# Preview Status
preview_status = tb.Label(right_panel, text="No preview loaded.", anchor="center")
preview_status.grid(row=2, column=0, pady=(44, 20))

# Language Buttons
btn_en = tb.Button(lang_frame, image=flag_uk_icon, bootstyle='light', command=lambda: set_language("en"),
                   cursor="hand2")
btn_en.grid(row=0, column=0, padx=3)
btn_pt = tb.Button(lang_frame, image=flag_br_icon, bootstyle="light", command=lambda: set_language("pt"),
                   cursor="hand2")
btn_pt.grid(row=0, column=1, padx=3)

# Preview Area
fig = plt.Figure(figsize=(5, 5.7), dpi=120)
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

canvas = FigureCanvasTkAgg(fig, master=preview_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# GUI Main Loop
mainwindow.mainloop()
