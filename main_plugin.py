# -*- coding: utf-8 -*-
"""
Plugin Principal: Observatorio Forestal UTN
Universidad Técnica del Norte (UTN)
Autor: Oscar Hernando Eraso Terán
Email: utn.sig@gmail.com
Sitio web: https://observatorioforestal.utn.edu.ec/

Integrado 100% nativo dentro del menú 'Complementos' de QGIS.
Sin interfaces gráficas complejas; ejecución directa y ágil de herramientas.
"""

import os
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.PyQt.QtGui import QIcon, QDesktopServices
from qgis.PyQt.QtCore import QUrl

from .core.logger import Logger
from .modules.imagenes.module import ImagenesModule
from .modules.incendios.module import IncendiosModule

class ObservatorioForestalUTNPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.plugin_menu = None
        self.modules = []
        self.about_action = None

    def initGui(self):
        """Inicializa las herramientas como parte nativa del menú Complementos."""
        Logger.info("Inicializando Observatorio Forestal UTN en menú Complementos...")

        icon_path = os.path.join(self.plugin_dir, "icons", "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        # 1. Crear submenú dentro del menú nativo de 'Complementos' (Plugins)
        self.plugin_menu = QMenu("Observatorio Forestal UTN", self.iface.mainWindow())
        self.plugin_menu.setIcon(icon)

        # 2. Módulo Imágenes (Imágenes Base nativas)
        self.mod_imagenes = ImagenesModule(self.iface, self.plugin_menu)
        self.modules.append(self.mod_imagenes)

        # 3. Módulo Incendios (Carga y Simbología FIRMS nativa)
        self.mod_incendios = IncendiosModule(self.iface, self.plugin_menu)
        self.modules.append(self.mod_incendios)

        # 4. Separador y Acceso a la Plataforma Web Institucional
        self.plugin_menu.addSeparator()

        self.about_action = QAction(icon, "Plataforma Web (Observatorio Forestal UTN)", self.iface.mainWindow())
        self.about_action.setToolTip("Abrir sitio web oficial: https://observatorioforestal.utn.edu.ec/")
        self.about_action.triggered.connect(self.open_web)
        self.plugin_menu.addAction(self.about_action)

        # 5. Insertar directamente en el menú 'Complementos' de QGIS
        self.iface.pluginMenu().addMenu(self.plugin_menu)

        Logger.success("Observatorio Forestal UTN integrado en menú Complementos exitosamente.")

    def open_web(self):
        """Abre la plataforma institucional en el navegador sin ventanas flotantes pesadas."""
        QDesktopServices.openUrl(QUrl("https://observatorioforestal.utn.edu.ec/"))
        self.iface.messageBar().pushInfo(
            "Observatorio Forestal UTN",
            "Abriendo plataforma web oficial: https://observatorioforestal.utn.edu.ec/"
        )

    def unload(self):
        """Descarga limpia del plugin al desactivarlo o recargarlo."""
        Logger.info("Descargando Observatorio Forestal UTN...")
        for mod in self.modules:
            mod.unload()

        if self.plugin_menu:
            self.iface.pluginMenu().removeAction(self.plugin_menu.menuAction())
