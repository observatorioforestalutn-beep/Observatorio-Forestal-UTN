# -*- coding: utf-8 -*-
"""
Simbología graduada térmica oficial NASA FIRMS para capas vectoriales de incendios.
Mantiene las capas compactas (sin desplegar la lista de rangos en el panel de capas).
"""

from qgis.core import (
    QgsMarkerSymbol, QgsRendererRange, QgsGraduatedSymbolRenderer, QgsProject
)
from qgis.utils import iface

NASA_TIME_EXPRESSION = """
with_variable(
    'mi_intervalo',
    age(
        now() + to_interval('5 hours'), 
        to_datetime(
            "acq_date" || ' ' || 
            left(lpad(to_string(to_int("acq_time")), 4, '0'), 2) || ':' || 
            right(lpad(to_string(to_int("acq_time")), 4, '0'), 2) || ':00'
        )
    ),
    abs(day(@mi_intervalo) * 24 + hour(@mi_intervalo) + minute(@mi_intervalo) / 60.0)
)
"""

NASA_RANGES = [
    (0, 1,    '#8b0000', 5.0, '< 1h (Frente muy activo)'),
    (1, 4,    '#cd0000', 4.0, '1 - 4h'),
    (4, 8,    '#ee2c2c', 3.2, '4 - 8h'),
    (8, 12,   '#ff4500', 2.5, '8 - 12h'),
    (12, 18,  '#ff8c00', 1.8, '12 - 18h'),
    (18, 24,  '#ffd700', 1.4, '18 - 24h'),
    (24, 999, '#ffffe0', 1.0, '> 24h (Residual)')
]

def apply_nasa_firms_symbology(layer):
    if not layer or layer.type() != 0:
        return False
        
    range_list = []
    for min_val, max_val, color, size, label in NASA_RANGES:
        sym = QgsMarkerSymbol.createSimple({
            'name': 'circle', 
            'color': color, 
            'outline_color': '0,0,0,30', 
            'outline_width': '0.1'
        })
        sym.setSize(size)
        qgs_range = QgsRendererRange(min_val, max_val, sym, label)
        range_list.append(qgs_range)
        
    renderer = QgsGraduatedSymbolRenderer(NASA_TIME_EXPRESSION, range_list)
    renderer.setMode(QgsGraduatedSymbolRenderer.Custom)
    
    layer.setRenderer(renderer)
    layer.setOpacity(0.95)
    layer.triggerRepaint()
    
    # Mantener la capa SIN DESPLEGAR (compacta, sin abrir los 7 rangos en la lista)
    node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
    if node:
        node.setExpanded(False)
        
    if iface:
        iface.layerTreeView().refreshLayerSymbology(layer.id())
    return True
