# Módulo: Capítulo 5 - Predicción de Tasa de Clics (CTR) con Regresión Logística

## Descripción

Este módulo aborda un problema clásico y fundamental en la industria de la publicidad digital (Ad-Tech): la **predicción de la Tasa de Clics (Click-Through Rate - CTR)**. El proyecto implementa un ciclo de vida completo de ciencia de datos, desde la definición del problema de negocio hasta la validación robusta y la recomendación final de un modelo predictivo.

El núcleo del proyecto es la implementación de un modelo de **Regresión Logística**, con un fuerte énfasis en el manejo de un **dataset severamente desbalanceado** y en la **interpretabilidad** de los resultados para la toma de decisiones. Se traducen y amplían los conceptos del libro a un pipeline de Python profesional y metodológicamente riguroso.

---

## Contenido Detallado

### Ejercicio 01: Predicción de CTR con Regresión Logística y Manejo de Desbalanceo

- **Objetivo:** Construir, optimizar y validar un modelo de clasificación binaria para predecir si un usuario hará clic en un anuncio. El proyecto se centra en manejar el desequilibrio de clases, optimizar métricas relevantes para el negocio (F1-Score) y extraer insights accionables del modelo final.
- **Metodología y Hallazgos Clave:**
    1. **Análisis de Costo de Error:** El proyecto se inicia con un análisis del problema de negocio, definiendo el alto costo de los **Falsos Negativos** (oportunidades de venta perdidas) como el principal factor a minimizar.
    2. **EDA e Identificación del Desafío:** El Análisis Exploratorio de Datos (EDA) confirma un severo desbalance de clases (solo **0.46% de clics**) y revela que la **recencia y recurrencia** de las visitas son los predictores más potentes.
    3. **Modelado Robusto con `Pipelines`:** Se utiliza `scikit-learn Pipelines` para encapsular el preprocesamiento y el modelado, garantizando la integridad de los datos. Se demuestra que un modelo base es inútil (0% Recall), mientras que un modelo con `class_weight='balanced'` logra capturar el **76%** de los clics.
    4. **Optimización del Umbral de Decisión:** Se demuestra que el umbral por defecto (0.5) es subóptimo. Se realiza una búsqueda sistemática para encontrar el **umbral (`0.95`) que maximiza el F1-Score**, logrando un equilibrio superior entre la eficiencia del gasto (Precision) y la captura de clientes (Recall).
    5. **Cuantificación del Impacto de Negocio:** El análisis de la **Curva de Lift** traduce el rendimiento del modelo en valor tangible, demostrando que al dirigirse al 10% de los usuarios con mayor probabilidad, se pueden obtener **6.67 veces más clics** que con una selección aleatoria.
    6. **Validación Avanzada y Descubrimiento Final:**
        - **Validación Cruzada:** Confirma la estabilidad del modelo, arrojando un **AUC promedio de 0.855**.
        - **Análisis de Calibración:** Concluye que el modelo es una excelente herramienta de **ranking**, pero no de estimación de probabilidades absolutas.
        - **Selección Secuencial de Características (SFS):** Este análisis revela el hallazgo más importante del proyecto: un **modelo más simple, con solo 10 de las 21 características, supera en rendimiento (AUC de 0.871)** al modelo completo, ofreciendo una solución más eficiente y robusta para producción.

- **Tecnologías:** Python, Jupyter Notebook, Pandas, `scikit-learn`, `matplotlib`, `seaborn`, `mlxtend`.
- **Archivo Principal:** [`notebooks/01-EDA-y-Preprocesamiento.ipynb`](./notebooks/01-EDA-y-Preprocesamiento.ipynb)
