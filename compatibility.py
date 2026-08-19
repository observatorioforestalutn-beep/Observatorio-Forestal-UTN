# -*- coding: utf-8 -*-
"""
Módulo de compatibilidad para QGIS 3.10 a QGIS 4.99, Qt5 y Qt6.
Centraliza las diferencias de API entre versiones para asegurar
estabilidad institucional a largo plazo.
"""

from qgis.core import Qgis, QgsApplication
from qgis.PyQt.QtCore import QObject

# Detección de versión de QGIS
QGIS_VERSION_INT = Qgis.QGIS_VERSION_INT

def is_qgis4():
    """Retorna True si se está ejecutando en QGIS 4.x o superior."""
    return QGIS_VERSION_INT >= 40000

def get_message_level(level_name):
    """
    Retorna el enum de MessageLevel compatible entre QGIS 3.x y QGIS 4.x.
    """
    level_name = level_name.lower()
    try:
        # QGIS 3.14+ y QGIS 4.x
        if hasattr(Qgis, 'MessageLevel'):
            if level_name == 'info':
                return Qgis.MessageLevel.Info
            elif level_name == 'warning':
                return Qgis.MessageLevel.Warning
            elif level_name == 'critical':
                return Qgis.MessageLevel.Critical
            elif level_name == 'success':
                return Qgis.MessageLevel.Success
    except Exception:
        pass

    # Fallback para QGIS 3.10
    if level_name == 'info':
        return getattr(Qgis, 'Info', 0)
    elif level_name == 'warning':
        return getattr(Qgis, 'Warning', 1)
    elif level_name == 'critical':
        return getattr(Qgis, 'Critical', 2)
    elif level_name == 'success':
        return getattr(Qgis, 'Success', 3)
    return 0
