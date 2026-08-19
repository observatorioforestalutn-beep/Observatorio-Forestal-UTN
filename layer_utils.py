# -*- coding: utf-8 -*-
"""
Utilidades nativas de gestión de capas y grupos en el lienzo de QGIS.
Garantiza que las capas base se ubiquen al fondo, las capas temáticas (FIRMS) arriba,
y permite el auto-encuadre automático centrado en Ecuador.
"""

from qgis.core import (
    QgsProject, QgsRectangle, QgsCoordinateReferenceSystem, QgsCoordinateTransform
)
from qgis.utils import iface

# Extensión geográfica optimizada de Ecuador (EPSG:4326)
ECUADOR_EXTENT_4326 = QgsRectangle(-84.40413, -6.68110, -71.87426, 2.84844)

def zoom_to_ecuador(force=False):
    """
    Auto-centra y ajusta el zoom del lienzo de QGIS en Ecuador.
    Si force=False, solo lo ejecuta si el proyecto estaba vacío o tiene pocas capas.
    """
    if iface is None:
        return
        
    canvas = iface.mapCanvas()
    project = QgsProject.instance()
    
    # Si no es forzado y ya hay muchas capas previas, respetar el encuadre del usuario
    if not force and len(project.mapLayers()) > 5:
        return

    try:
        dest_crs = canvas.mapSettings().destinationCrs()
        if not dest_crs.isValid():
            dest_crs = project.crs()
            if not dest_crs.isValid():
                dest_crs = QgsCoordinateReferenceSystem("EPSG:4326")
            
        src_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transform = QgsCoordinateTransform(src_crs, dest_crs, project)
        
        transformed_extent = transform.transformBoundingBox(ECUADOR_EXTENT_4326)
        canvas.setExtent(transformed_extent)
        canvas.refresh()
    except Exception as e:
        pass

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
