# Observatorio Forestal UTN — Plugin para QGIS

[![QGIS Version](https://img.shields.io/badge/QGIS-3.10%20--%204.99-success.svg)](https://qgis.org/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Institution](https://img.shields.io/badge/Instituci%C3%B3n-UTN%20--%20Ecuador-1b5e20.svg)](https://observatorioforestal.utn.edu.ec/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Observatorio--Forestal--UTN-181717?logo=github)](https://github.com/observatorioforestalutn-beep/Observatorio-Forestal-UTN)

Plugin institucional desarrollado para el **Observatorio Forestal de la Universidad Técnica del Norte (UTN)** en Ibarra, Ecuador. Proporciona un ecosistema ágil, modular y 100% nativo para el monitoreo satelital en tiempo real de incendios forestales, teledetección y gestión de recursos forestales.

---

## 📌 Datos Institucionales y Autoría

* **Institución:** Universidad Técnica del Norte (UTN) — Ecuador
* **Autor Responsable:** PhD. Oscar Hernando Eraso Terán (Docente Investigador)
* **Correos Electrónicos:** [observatorioforestalutn@gmail.com](mailto:observatorioforestalutn@gmail.com) | [oheraso@utn.edu.ec](mailto:oheraso@utn.edu.ec)
* **Plataforma Web Oficial:** [https://observatorioforestal.utn.edu.ec/](https://observatorioforestal.utn.edu.ec/)
* **Repositorio en GitHub:** [observatorioforestalutn-beep/Observatorio-Forestal-UTN](https://github.com/observatorioforestalutn-beep/Observatorio-Forestal-UTN)
* **Seguimiento de Errores / Issues:** [GitHub Issues](https://github.com/observatorioforestalutn-beep/Observatorio-Forestal-UTN/issues)

---

## 🚀 Funcionalidades Principales

### 🔥 1. Monitoreo de Incendios en Tiempo Real (NASA FIRMS)
* **Carga en 1 Clic:** Importa y agrupa de forma automática todas las fuentes satelitales activas de las últimas 24 horas para Sudamérica:
  * **MODIS** (Terra y Aqua) — WFS
  * **VIIRS S-NPP** (375m) — WFS
  * **VIIRS NOAA-20** (375m) — WFS
  * **VIIRS NOAA-21** (375m) — WFS
  * **FIRMS Térmico Global** — WMS Ráster
* **Simbología Temporal Oficial de la NASA:** Clasificación graduada de 7 escalones temporales calculados de forma dinámica y continua en horas:
  * 🔴 **< 1 hora:** Rojo oscuro gigante (Frente activo de avance rápido)
  * 🔴 **1 - 4 horas:** Rojo intenso
  * 🟠 **4 - 8 horas:** Naranja rojizo
  * 🟠 **8 - 12 horas:** Naranja
  * 🟡 **12 - 18 horas:** Ámbar
  * 🟡 **18 - 24 horas:** Amarillo
  * ⚪ **> 24 horas:** Amarillo crema/residual
* **Auto-Refresco Dinámico (5 Minutos):** Consulta en segundo plano los servidores de la NASA cada 5 minutos, incorporando nuevos focos de calor y actualizando la degradación de color de los existentes sin recargar manualmente.
* **Jerarquía Inteligente:** Ubica el grupo `FIRMS` siempre al tope del árbol de capas y mantiene la leyenda compacta y ordenada.
* **Auto-Encuadre en Ecuador:** Centra y ajusta el zoom automáticamente sobre el territorio ecuatoriano al cargarse en lienzos limpios.

### 🗺️ 2. Imágenes Base (Mosaicos Satelitales y Cartografía)
* Acceso instantáneo a capas base de alta resolución ordenadas alfabéticamente:
  * 🛰️ **Bing Satellite**
  * 🛰️ **Google Hybrid** (Satélite + Etiquetas)
  * 🗺️ **Google Road** (Vías y callejero)
  * 🏔️ **OpenTopoMap** (Relieve y curvas de nivel)
  * 🌐 **OSM Standard** (OpenStreetMap)
* **Posicionamiento Automático al Fondo:** Se insertan siempre en la parte inferior del árbol de capas para no obstruir vectores ni capas temáticas.
* **Cero Dependencias:** Utiliza el proveedor nativo `wms` de QGIS con soporte optimizado para teselas XYZ.

---

## 🏛️ Principios de Arquitectura y Rendimiento

1. **Prioridad QGIS Nativo:**
   $$\text{QGIS Nativo} > \text{Processing Nativo} > \text{GDAL Integrado} > \text{PyQGIS} > \text{Dependencias Externas}$$
2. **Cero Dependencias Pesadas:** Sin descargas de paquetes adicionales, bibliotecas externas ni APIs bloqueantes.
3. **Compatibilidad Total (QGIS 3.10 a QGIS 4.99):**
   * Totalmente compatible con **Qt5 / Qt6** y **Python 3.10 / 3.11 / 3.12**.
   * Importaciones centralizadas mediante `qgis.PyQt`.
4. **Diseño Modular y Escalable:** Arquitectura desacoplada preparada para la incorporación progresiva de nuevos módulos sin reestructuración.

---

## 📂 Estructura del Proyecto

```text
Observatorio_Forestal_UTN/
│
├── __init__.py                                 # Fábrica del plugin (classFactory)
├── metadata.txt                               # Metadatos institucionales y compatibilidad
├── main_plugin.py                             # Integración en el menú 'Complementos'
├── README.md                                  # Documentación técnica y guía de usuario
│
├── core/                                      # Núcleo y utilidades comunes
│   ├── compatibility.py                       # Capa de compatibilidad QGIS 3 y QGIS 4
│   ├── layer_utils.py                         # Gestión de jerarquía y auto-zoom a Ecuador
│   ├── logger.py                              # Registro centralizado mediante QgsMessageLog
│   └── settings.py                            # Persistencia nativa con QgsSettings
│
├── icons/                                     # Recursos gráficos e identidad UTN
│   ├── icon.png                               # Ícono oficial (128x128 px)
│   ├── icon64.png / icon32.png / icon16.png   # Escalas optimizadas
│   └── logo_utn.png                           # Logo institucional
│
├── modules/                                   # Módulos temáticos independientes
│   ├── imagenes/                              # Módulo de Imágenes Base y Teledetección
│   │   ├── base_maps.py                       # Conexiones XYZ codificadas
│   │   ├── module.py                          # Controlador de menús de imágenes
│   │   └── algorithms/                        # Espacio para algoritmos futuros
│   │
│   └── incendios/                             # Módulo de Monitoreo de Incendios
│       ├── firms_loader.py                    # Carga y auto-refresco de WFS/WMS
│       ├── symbology.py                       # Simbología matemática temporal NASA FIRMS
│       ├── module.py                          # Controlador de acciones de incendios
│       └── algorithms/                        # Espacio para algoritmos futuros (dNBR, cicatrices)
│
└── ui/                                        # Componentes de interfaz
    └── about_dialog.py                        # Diálogo institucional con enlaces a GitHub y Web
```

---

## 💻 Instalación Manual

1. Descargue o clone el repositorio en el directorio de complementos de su perfil de QGIS:
   ```bash
   git clone https://github.com/observatorioforestalutn-beep/Observatorio-Forestal-UTN.git Observatorio_Forestal_UTN
   ```
   O copie la carpeta `Observatorio_Forestal_UTN` en:
   * **Windows:**
     ```text
     %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\Observatorio_Forestal_UTN
     ```
     *(o en `QGIS4` según la versión).*
   * **Linux:**
     ```bash
     ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/Observatorio_Forestal_UTN
     ```
   * **macOS:**
     ```bash
     ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/Observatorio_Forestal_UTN
     ```
2. Abra QGIS y diríjase a **Complementos > Administrar e instalar complementos...**
3. En la pestaña **Instalados**, busque `Observatorio Forestal UTN` y marque la casilla de activación.
4. El plugin se integrará inmediatamente en el menú superior **Complementos > Observatorio Forestal UTN**.

---

## 🗺️ Guía de Uso Rápido

1. **Para cargar un mapa base:**
   * Menú: `Complementos` $\rightarrow$ `Observatorio Forestal UTN` $\rightarrow$ `Imágenes Base` $\rightarrow$ Seleccionar capa (*ej. Google Hybrid*).
2. **Para monitorear incendios activos:**
   * Menú: `Complementos` $\rightarrow$ `Observatorio Forestal UTN` $\rightarrow$ `Incendios` $\rightarrow$ `Cargar FIRMS Activos (24h Sudamérica)`.
   * El mapa se centrará en Ecuador, cargará las detecciones satelitales recientes y se actualizará automáticamente cada 5 minutos.
3. **Para acceder al portal web o repositorio:**
   * Menú: `Complementos` $\rightarrow$ `Observatorio Forestal UTN` $\rightarrow$ `Plataforma Web (Observatorio Forestal UTN)`.

---

## 🔮 Hoja de Ruta (Futuras Versiones)

* [ ] **Teledetección Forestal:** Composición RGB masiva y cálculo de índices espectrales (NDVI, NBR, NBR2, CSI, NDWI) con `QgsRasterCalculator`.
* [ ] **Delimitación y Severidad de Cicatrices:** Algoritmo nativo de delimitación por lotes y severidad de quema (dNBR / RBR).
* [ ] **Descarga Automatizada:** Conectores con catálogos STAC (Sentinel-2 y Landsat).
* [ ] **Estadísticas Cantonales:** Resumen automático de áreas afectadas por incendios en la provincia de Imbabura y a nivel nacional.

---

## 📄 Licencia

Este proyecto está bajo la Licencia Pública General de GNU v3.0 (GPLv3).  
Desarrollado para la **Universidad Técnica del Norte (UTN)** — Ecuador.
