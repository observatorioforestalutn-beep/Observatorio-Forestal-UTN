# -*- coding: utf-8 -*-
"""
Definición de capas de imágenes base (XYZ Tiles) ordenadas alfabéticamente.
URLs codificadas para compatibilidad total con proveedores como Google, Bing y OSM.
Auto-centrado en Ecuador cuando se carga en un lienzo nuevo.
"""

from qgis.core import QgsRasterLayer, QgsProject
from ...core.logger import Logger
from ...core.layer_utils import add_base_map_to_bottom, zoom_to_ecuador

BASE_MAPS = {
    "Bing Satellite": {
        "url": "type=xyz&zmin=1&zmax=19&url=http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1",
        "name": "Bing Satellite"
    },
    "Google Hybrid": {
        "url": "type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Dy%26x%3D{x}%26y%3D{y}%26z%3D{z}",
        "name": "Google Hybrid"
    },
    "Google Road": {
        "url": "type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Dm%26x%3D{x}%26y%3D{y}%26z%3D{z}",
        "name": "Google Road"
    },
    "OpenTopoMap": {
        "url": "type=xyz&zmin=1&zmax=17&url=https://tile.opentopomap.org/{z}/{x}/{y}.png",
        "name": "OpenTopoMap"
    },
    "OSM Standard": {
        "url": "type=xyz&zmin=0&zmax=19&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "name": "OSM Standard"
    }
}

def load_base_map(map_key):
    if map_key not in BASE_MAPS:
        Logger.warning(f"Capa base '{map_key}' no encontrada.")
        return None
    
    info = BASE_MAPS[map_key]
    layer_name = info["name"]
    layer_url = info["url"]
    
    project = QgsProject.instance()
    is_first_layer = len(project.mapLayers()) == 0
    
    existing = project.mapLayersByName(layer_name)
    if existing:
        Logger.info(f"La capa base '{layer_name}' ya está cargada.")
        return existing[0]
    
    layer = QgsRasterLayer(layer_url, layer_name, "wms")
    if not layer.isValid():
        Logger.critical(f"No se pudo cargar '{layer_name}'. Verifica tu conexión a internet.")
        return None
    
    # Ubicar SIEMPRE abajo de todo en el árbol de capas
    add_base_map_to_bottom(layer)
    
    # Auto-centrar en Ecuador si es la primera capa cargada
    if is_first_layer:
        zoom_to_ecuador(force=True)
        
    Logger.success(f"Capa base '{layer_name}' cargada y encuadrada en Ecuador.")
    return layer
