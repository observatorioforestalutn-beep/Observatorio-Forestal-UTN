# -*- coding: utf-8 -*-
"""
Carga automática con 1 solo clic de todas las capas activas de NASA FIRMS.
Ubica el grupo FIRMS arriba, mantiene las capas compactas y auto-centra en Ecuador.
"""

from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject
from qgis.utils import iface
from ...core.logger import Logger
from ...core.layer_utils import get_or_create_top_group, add_layer_to_top_group, zoom_to_ecuador
from .symbology import apply_nasa_firms_symbology

FIRMS_GROUP_NAME = "FIRMS"
AUTO_REFRESH_INTERVAL_MINUTES = 5

FIRMS_LAYERS_CONFIG = [
    {
        "type": "vector",
        "name": "South America MODIS 24hrs fires/hotspots",
        "provider": "WFS",
        "source": "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:fires_modis_24hrs' url='https://firms.modaps.eosdis.nasa.gov/mapserver/wfs/South_America/30ae0fa1e8bbb56e9cdf34778d8b6bb9' version='auto'"
    },
    {
        "type": "vector",
        "name": "South America VIIRS S-NPP 24hrs fires/hotspots",
        "provider": "WFS",
        "source": "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:fires_snpp_24hrs' url='https://firms.modaps.eosdis.nasa.gov/mapserver/wfs/South_America/30ae0fa1e8bbb56e9cdf34778d8b6bb9' version='auto'"
    },
    {
        "type": "vector",
        "name": "South America VIIRS NOAA-21 24hrs fires/hotspots",
        "provider": "WFS",
        "source": "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:fires_noaa21_24hrs' url='https://firms.modaps.eosdis.nasa.gov/mapserver/wfs/South_America/30ae0fa1e8bbb56e9cdf34778d8b6bb9' version='auto'"
    },
    {
        "type": "vector",
        "name": "South America VIIRS NOAA-20 24hrs fires/hotspots",
        "provider": "WFS",
        "source": "pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:4326' typename='ms:fires_noaa20_24hrs' url='https://firms.modaps.eosdis.nasa.gov/mapserver/wfs/South_America/30ae0fa1e8bbb56e9cdf34778d8b6bb9' version='auto'"
    },
    {
        "type": "raster",
        "name": "FIRMS_24_hrs",
        "provider": "wms",
        "source": "crs=EPSG:4326&dpiMode=7&format=image/png&layers=fires_viirs_24&styles&tilePixelRatio=0&url=https://firms.modaps.eosdis.nasa.gov/mapserver/wms/fires/180914ebc4017e6f4e522b5324c79913"
    }
]

def enable_layer_auto_refresh(layer, minutes=AUTO_REFRESH_INTERVAL_MINUTES):
    try:
        if hasattr(layer, 'setAutoRefreshInterval') and hasattr(layer, 'setAutoRefreshEnabled'):
            interval_ms = int(minutes * 60 * 1000)
            layer.setAutoRefreshInterval(interval_ms)
            layer.setAutoRefreshEnabled(True)
    except Exception:
        pass

def load_all_firms_with_symbology():
    Logger.info("Cargando capas NASA FIRMS...")
    project = QgsProject.instance()
    
    # Verificar si es proyecto nuevo / inicial
    is_initial_load = len(project.mapLayers()) <= 1

    firms_group = get_or_create_top_group(FIRMS_GROUP_NAME)
    firms_group.setExpanded(True)

    for config in FIRMS_LAYERS_CONFIG:
        layer_name = config["name"]
        existing = project.mapLayersByName(layer_name)
        if existing:
            layer = existing[0]
        else:
            if config["type"] == "vector":
                layer = QgsVectorLayer(config["source"], layer_name, config["provider"])
            else:
                layer = QgsRasterLayer(config["source"], layer_name, config["provider"])
                
            if not layer.isValid():
                Logger.warning(f"No se pudo conectar a '{layer_name}'.")
                continue
                
            add_layer_to_top_group(layer, FIRMS_GROUP_NAME)

        if config["type"] == "vector":
            apply_nasa_firms_symbology(layer)

        enable_layer_auto_refresh(layer, AUTO_REFRESH_INTERVAL_MINUTES)

    # Re-asegurar orden y colapsar los nodos de cada capa
    firms_group = get_or_create_top_group(FIRMS_GROUP_NAME)
    for child in firms_group.children():
        child.setExpanded(False)

    # Auto-centrar en Ecuador en carga inicial
    if is_initial_load:
        zoom_to_ecuador(force=True)

    if iface:
        iface.mapCanvas().refreshAllLayers()
        iface.messageBar().pushSuccess(
            "Observatorio Forestal UTN",
            "Capas NASA FIRMS cargadas y centradas en Ecuador."
        )
    Logger.success("NASA FIRMS completado con auto-centrado en Ecuador.")
