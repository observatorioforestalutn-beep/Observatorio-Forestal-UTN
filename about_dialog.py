# -*- coding: utf-8 -*-
"""
Diálogo institucional 'Acerca de' para el Observatorio Forestal UTN.
Compatible con Qt6 / QGIS 4 y QGIS 3.
"""

import os
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from qgis.PyQt.QtGui import QPixmap, QDesktopServices
from qgis.PyQt.QtCore import Qt, QUrl

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca del Observatorio Forestal UTN")
        self.setFixedSize(520, 460)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Logo Institucional
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_dir = os.path.dirname(os.path.dirname(__file__))
        logo_path = os.path.join(current_dir, "icons", "logo_utn.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            logo_label.setPixmap(pix.scaledToWidth(360, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(logo_label)

        # Texto Institucional
        info_label = QLabel(
            "<h2 style='text-align: center; color: #1b5e20; margin-bottom: 2px;'>Observatorio Forestal UTN</h2>"
            "<p style='text-align: center; font-weight: bold; margin-top: 0;'>Plugin Institucional para QGIS (v1.0.0)</p>"
            "<hr style='border: 1px solid #c8e6c9;'>"
            "<p><b>Institución:</b> Universidad Técnica del Norte (UTN) — Ecuador</p>"
            "<p><b>Autor Responsable:</b> PhD. Oscar Hernando Eraso Terán<br>"
            "<span style='color: #555;'>Docente Investigador — Universidad Técnica del Norte</span></p>"
            "<p><b>Contacto:</b> <a href='mailto:observatorioforestalutn@gmail.com'>observatorioforestalutn@gmail.com</a> | <a href='mailto:oheraso@utn.edu.ec'>oheraso@utn.edu.ec</a></p>"
            "<p><b>Plataforma Web:</b> <a href='https://observatorioforestal.utn.edu.ec/'>https://observatorioforestal.utn.edu.ec/</a></p>"
            "<p><b>Repositorio GitHub:</b> <a href='https://github.com/observatorioforestalutn-beep/Observatorio-Forestal-UTN'>observatorioforestalutn-beep/Observatorio-Forestal-UTN</a></p>"
        )
        info_label.setOpenExternalLinks(True)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Botones
        btn_layout = QHBoxLayout()
        web_btn = QPushButton("Plataforma Web")
        web_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://observatorioforestal.utn.edu.ec/")))
        btn_layout.addWidget(web_btn)

        gh_btn = QPushButton("GitHub")
        gh_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/observatorioforestalutn-beep/Observatorio-Forestal-UTN")))
        btn_layout.addWidget(gh_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)
