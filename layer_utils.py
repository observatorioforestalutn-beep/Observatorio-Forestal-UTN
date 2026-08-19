# -*- coding: utf-8 -*-
"""
Utilidades nativas de gestión de capas y grupos en el lienzo de QGIS.
Garantiza que las capas base se ubiquen al fondo, las capas temáticas (FIRMS) arriba,
establece el CRS del proyecto a EPSG:4326 (WGS 84) y auto-centra en Ecuador.
"""

from qgis.core import (
    QgsProject, QgsRectangle, QgsCoordinateReferenceSystem, QgsCoordinateTransform
)
from qgis.utils import iface

# Extensión geográfica optimizada de Ecuador en WGS 84 (EPSG:4326)
ECUADOR_EXTENT_4326 = QgsRectangle(-84.40413, -6.68110, -71.87426, 2.84844)

def set_project_crs_and_zoom_to_ecuador(force_crs=True, force_zoom=True):
    """
    1. Establece el sistema de coordenadas de referencia (CRS) del proyecto a EPSG:4326 (WGS 84).
    2. Auto-centra y ajusta el zoom del lienzo de QGIS directamente en Ecuador.
    """
    project = QgsProject.instance()
    crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    # 1. Forzar CRS del proyecto a EPSG:4326
    if force_crs or project.crs().authid() != "EPSG:4326":
        project.setCrs(crs_4326)

    # 2. Ajustar extensión del mapa centrada en Ecuador
    if iface and force_zoom:
        canvas = iface.mapCanvas()
        canvas.setDestinationCrs(crs_4326)
        canvas.setExtent(ECUADOR_EXTENT_4326)
        canvas.refresh()

def zoom_to_ecuador(force=False):
    """
    Función de compatibilidad para auto-centrar en Ecuador y asegurar EPSG:4326.
    """
    set_project_crs_and_zoom_to_ecuador(force_crs=True, force_zoom=force)

def get_or_create_top_group(group_name):
    """
    Obtiene un grupo de capas o lo crea ubicándolo SIEMPRE en la parte superior (índice 0).
    Si ya existe, lo mueve al tope del árbol de capas.
    """
    root = QgsProject.instance().layerTreeRoot()
    group = root.findGroup(group_name)
    if group is None:
        group = root.insertGroup(0, group_name)
    else:
        try:
            current_idx = root.children().index(group)
            if current_idx != 0:
                clone = group.clone()
                root.insertChildNode(0, clone)
                root.removeChildNode(group)
                group = clone
        except Exception:
            pass
    return group

def add_layer_to_top_group(layer, group_name):
    """
    Agrega una capa a un grupo situado en la parte superior del árbol de capas.
    """
    project = QgsProject.instance()
    project.addMapLayer(layer, False)
    group = get_or_create_top_group(group_name)
    group.addLayer(layer)

def add_base_map_to_bottom(layer):
    """
    Agrega una capa base (ráster XYZ/WMS) al FONDO de todas las capas del proyecto.
    """
    project = QgsProject.instance()
    project.addMapLayer(layer, False)
    root = project.layerTreeRoot()
    root.addLayer(layer)
