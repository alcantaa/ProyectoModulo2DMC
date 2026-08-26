# 📊 EDA — Bank Marketing Campaign

Aplicación interactiva construida en **Python + Streamlit** para el
**Análisis Exploratorio de Datos (EDA)** de la última campaña de marketing
telefónico de una institución financiera.

> **Caso de Estudio N°1** — Especialización en Python for Analytics, DMC Institute
> Docente: MSc. Carlos Carrillo Villavicencio

---

## 👤 Datos del autor

- **Nombre completo:** Alexander Alcantara
- **Curso / Especialización:** Especialización en Python for Analytics — DMC Institute
- **Año:** 2026

---

## 🎯 Descripción del proyecto

La institución financiera vio caer la efectividad de sus campañas de
marketing telefónico de **12% a 8%** en los últimos 6 meses. Este proyecto
analiza los datos de la última campaña (`BankMarketing.csv`, 41,188
registros / 21 variables) para identificar relaciones y patrones entre
variables demográficas, del contacto y del contexto macroeconómico, que
sirvan de base para la **toma de decisiones comerciales**.

> El objetivo **no** es construir un modelo predictivo, sino aplicar de
> forma integrada conceptos de Python, Pandas, NumPy, POO, estadística
> descriptiva y visualización de datos, en una herramienta tipo producto
> analítico real.

### Estructura de la aplicación

| Módulo | Contenido |
|---|---|
| 🏠 Home | Presentación del proyecto, objetivo, autor y dataset |
| 📂 Carga del dataset | `st.file_uploader`, validación, vista previa y dimensiones |
| 🔍 EDA | 10 ítems de análisis organizados en `st.tabs` |
| ✅ Conclusiones | 5 conclusiones orientadas a la toma de decisiones |

**Ítems del EDA:** información general · clasificación de variables ·
estadísticas descriptivas · valores faltantes · distribución de numéricas ·
variables categóricas · bivariado numérico-categórico · bivariado
categórico-categórico · análisis dinámico con parámetros del usuario ·
hallazgos clave.

### Tecnologías utilizadas

- **Python 3**
- **Streamlit** — interfaz interactiva
- **Pandas / NumPy** — manipulación y análisis de datos
- **Matplotlib / Seaborn** — visualización
- **Programación Orientada a Objetos** — clase `DataAnalyzer`, que
  encapsula clasificación de variables, estadísticas descriptivas y
  funciones de visualización

---


---

## 📁 Contenido del repositorio

```
├── app.py              # Aplicación Streamlit principal
├── requirements.txt    # Dependencias del proyecto
├── BankMarketing.csv   # Dataset utilizado
└── README.md           # Este archivo
