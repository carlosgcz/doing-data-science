# Módulo: Capítulo 2 - Análisis Exploratorio de Datos (EDA)

## Descripción

Este módulo se enfoca en los fundamentos del Análisis Exploratorio de Datos (EDA), tal como se presenta en el Capítulo 2 de *Doing Data Science*. El objetivo es limpiar, visualizar y generar hipótesis iniciales a partir de datasets crudos. Una característica clave de este módulo es la implementación paralela de los análisis en **R (con ggplot2)** y **Python (con seaborn)**, demostrando cómo diferentes herramientas pueden usarse para lograr los mismos objetivos de análisis y validando la consistencia de los hallazgos.

---

## Contenido Detallado

### **Exercise 01: EDA en Datos de Publicidad (NYT)**

- **Objetivo:** Analizar los datos de impresiones y clics de anuncios del New York Times para entender el comportamiento del usuario. El análisis busca identificar patrones demográficos, calcular el Click-Through Rate (CTR) y descubrir anomalías en los datos.
- **Metodología:**
    1. **Análisis de un solo día:** Se realiza un EDA inicial sobre un único archivo (`nyt1.csv`) para establecer una línea base.
    2. **Automatización del análisis:** Se crea un script para procesar los 31 días de datos, agregando los resultados para un análisis longitudinal.
    3. **Hallazgos Clave:**
        - Se identificó un grupo de usuarios "Invalid" (Edad ≤ 0) con un **CTR casi el doble** que el de los usuarios válidos.
        - La proporción de este grupo "Invalid" es un factor dominante que explica las fluctuaciones del CTR global a lo largo del mes.
        - Los usuarios mayores de 65 años muestran un CTR consistentemente más alto que otros grupos de edad.
    4. **Implementación Dual:** Todo el análisis se replica en R y Python para asegurar la reproducibilidad y comparar las capacidades de visualización de `ggplot2` y `seaborn`.
- **Tecnologías:** R, Python, ggplot2, seaborn, dplyr, pandas.
- **Notebooks:**
  - [`notebook/eda_nyt.Rmd`](./notebook/eda_nyt.Rmd) y [`notebook/eda_nyt.ipynb`](./notebook/eda_nyt.ipynb) (Análisis de un día)
  - [`notebook/automate_nyt_analysis.Rmd`](./notebook/automate_nyt_analysis.Rmd) y [`notebook/automate_nyt.ipynb`](./notebook/automate_nyt.ipynb) (Análisis multidiario)

### **Exercise 02: Limpieza y EDA del Mercado Inmobiliario (Manhattan)**

- **Objetivo:** Tomar un dataset desordenado del mundo real (`rollingsales_manhattan.xls`), realizar una limpieza exhaustiva y prepararlo para análisis posteriores.
- **Metodología:**
    1. **Carga y Limpieza:** Se carga el archivo Excel y se aplican técnicas de *data wrangling* para corregir tipos de datos, manejar valores faltantes y estandarizar formatos.
    2. **Análisis Exploratorio Inicial:** Se generan estadísticas descriptivas y visualizaciones para entender la distribución de precios, tipos de propiedades y otras características clave.
    3. **Preparación para Modelado:** Este notebook sirve como el pre-procesamiento fundamental para los modelos de regresión y clasificación que se desarrollan en el **Capítulo 3**.
- **Tecnologías:** Python, pandas, seaborn.
- **Notebook:** [`notebook/manhattan_analysis.ipynb`](./notebook/manhattan_analysis.ipynb)

### **Documento Adicional: Estrategia de Datos RealDirect**

- **Descripción:** Un documento de texto que resume la estrategia de datos propuesta para la empresa ficticia RealDirect, proporcionando contexto de negocio para el análisis del mercado inmobiliario.
- **Archivo:** [`notebook/realdirect_strategy.md`](./notebook/realdirect_strategy.md)

---
