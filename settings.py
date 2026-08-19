# -*- coding: utf-8 -*-
"""
Manejo de configuración persistente utilizando QgsSettings nativo.
"""

from qgis.core import QgsSettings

SETTINGS_PREFIX = "ObservatorioForestalUTN/"

class PluginSettings:
    @staticmethod
    def get(key, default_value=None):
        settings = QgsSettings()
        return settings.value(SETTINGS_PREFIX + key, default_value)

    @staticmethod
    def set(key, value):
        settings = QgsSettings()
        settings.setValue(SETTINGS_PREFIX + key, value)
