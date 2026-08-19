# -*- coding: utf-8 -*-
"""
Módulo nativo de 'Incendios' del Observatorio Forestal UTN.
Carga directa en 1 clic con simbología temporal oficial NASA FIRMS.
"""

from qgis.PyQt.QtWidgets import QAction
from .firms_loader import load_all_firms_with_symbology

class IncendiosModule:
    def __init__(self, iface, parent_menu):
        self.iface = iface
        self.parent_menu = parent_menu
        self.menu = None
        self.init_ui()

    def init_ui(self):
        # Crear submenú para la categoría Incendios
        self.menu = self.parent_menu.addMenu("Incendios")
        
        # Herramienta única directa: Cargar todos los FIRMS con 1 clic
        action_load_firms = QAction("Cargar FIRMS Activos (24h Sudamérica)", self.iface.mainWindow())
        action_load_firms.setToolTip("Carga en 1 clic los servicios WFS y WMS de MODIS/VIIRS y aplica la simbología graduada de tiempo oficial NASA FIRMS.")
        action_load_firms.triggered.connect(load_all_firms_with_symbology)
        self.menu.addAction(action_load_firms)

    def unload(self):
        pass
