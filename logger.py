# -*- coding: utf-8 -*-
"""
Sistema de registro y logging centralizado para el Observatorio Forestal UTN.
Utiliza QgsMessageLog nativo de QGIS sin dependencias externas.
"""

from qgis.core import QgsMessageLog
from .compatibility import get_message_level

PLUGIN_TAG = "Observatorio Forestal UTN"

class Logger:
    @staticmethod
    def info(message):
        QgsMessageLog.logMessage(str(message), PLUGIN_TAG, get_message_level('info'))

    @staticmethod
    def warning(message):
        QgsMessageLog.logMessage(str(message), PLUGIN_TAG, get_message_level('warning'))

    @staticmethod
    def critical(message):
        QgsMessageLog.logMessage(str(message), PLUGIN_TAG, get_message_level('critical'))

    @staticmethod
    def success(message):
        QgsMessageLog.logMessage(str(message), PLUGIN_TAG, get_message_level('success'))
