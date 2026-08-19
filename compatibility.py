# -*- coding: utf-8 -*-
"""
Módulo de compatibilidad para QGIS 3.10 a QGIS 4.99, Qt5 y Qt6.
Centraliza las diferencias de API entre versiones para asegurar
estabilidad institucional a largo plazo.
"""

from qgis.core import Qgis

QGIS_VERSION_INT = Qgis.QGIS_VERSION_INT

def is_qgis4():
    """Retorna True si se está ejecutando en QGIS 4.x o superior."""
    return QGIS_VERSION_INT >= 40000

def get_message_level(level_name):
    """
    Retorna el enum de MessageLevel compatible entre QGIS 3.x y QGIS 4.x
    utilizando inspección segura de atributos sin excepciones silenciosas.
    """
    level_name = level_name.lower()
    
    # QGIS 3.14+ y QGIS 4.x
    if hasattr(Qgis, 'MessageLevel'):
        msg_lvl = getattr(Qgis, 'MessageLevel')
        if level_name == 'info' and hasattr(msg_lvl, 'Info'):
            return msg_lvl.Info
        elif level_name == 'warning' and hasattr(msg_lvl, 'Warning'):
            return msg_lvl.Warning
        elif level_name == 'critical' and hasattr(msg_lvl, 'Critical'):
            return msg_lvl.Critical
        elif level_name == 'success' and hasattr(msg_lvl, 'Success'):
            return msg_lvl.Success

    # Fallback compatible con QGIS 3.10
    if level_name == 'info':
        return getattr(Qgis, 'Info', 0)
    elif level_name == 'warning':
        return getattr(Qgis, 'Warning', 1)
    elif level_name == 'critical':
        return getattr(Qgis, 'Critical', 2)
    elif level_name == 'success':
        return getattr(Qgis, 'Success', 3)
    
    return 0
