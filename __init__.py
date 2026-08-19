# -*- coding: utf-8 -*-
"""
Plugin Institucional: Observatorio Forestal UTN
Universidad Técnica del Norte (UTN) — Ecuador
Autor: Oscar Hernando Eraso Terán (Docente Investigador)
Email: oheraso@utn.edu.ec
Sitio web: https://observatorioforestal.utn.edu.ec/
"""

from .main_plugin import ObservatorioForestalUTNPlugin

def classFactory(iface):
    """Factory method to load the plugin instance into QGIS."""
    return ObservatorioForestalUTNPlugin(iface)
