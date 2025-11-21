# Módulo: Capítulo 5 - Predicción de Tasa de Clics (CTR) con Regresión Logística

## Descripción

Este módulo aborda un problema clásico y fundamental en la industria de la publicidad digital (Ad‑Tech): la predicción de la Tasa de Clics (Click‑Through Rate — CTR). Implementa un ciclo de vida completo de ciencia de datos, desde la definición del problema de negocio hasta la validación robusta y la recomendación final de un modelo predictivo.  
El núcleo del proyecto es una Regresión Logística, con énfasis en el manejo de un dataset severamente desbalanceado y en la interpretabilidad para la toma de decisiones. Se traduce y amplía el contenido del libro en un pipeline de Python profesional y metodológicamente riguroso.

---

## Contenido detallado

### Ejercicio 01: Predicción de CTR con Regresión Logística y manejo de desbalanceo

- Objetivo:
  - Construir, optimizar y validar un modelo de clasificación binaria para predecir si un usuario hará clic en un anuncio, priorizando métricas de negocio (F1‑Score) y el manejo del desequilibrio de clases.
- Metodología y hallazgos clave:
    1. Análisis de costo de error: se identifica el alto costo de los falsos negativos como variable crítica a minimizar.
    2. EDA: se confirma un severo desbalance (≈ 0.46% de clics). La recencia y recurrencia de visitas son los predictores más fuertes.
    3. Pipelines: uso de `scikit-learn` Pipelines para encapsular preprocesamiento y modelado. El modelo base falla (Recall 0%), mientras que `class_weight='balanced'` captura ~76% de los clics.
    4. Optimización de umbral: el umbral por defecto (0.5) es subóptimo; se encuentra un umbral óptimo de ~0.95 que maximiza el F1‑Score, equilibrando Precision y Recall.
    5. Curva de Lift: dirigirse al 10% superior de usuarios produce ~6.67× más clics que una selección aleatoria.
    6. Validación avanzada:
         - Validación cruzada: AUC promedio ≈ 0.855.
         - Calibración: el modelo funciona muy bien como ranking, pero no para estimar probabilidades absolutas.
         - Selección secuencial de características (SFS): un modelo simple con 10 de 21 características mejora el rendimiento (AUC ≈ 0.871), siendo más eficiente para producción.
- Tecnologías: Python, Jupyter Notebook, Pandas, `scikit-learn`, `matplotlib`, `seaborn`, `mlxtend`.
- Archivo principal: `notebooks/01-EDA-y-Preprocesamiento.ipynb`

### Ejercicio 02: Validación del Modelo Campeón, escalabilidad y despliegue

- **Objetivo:**
  - Llevar el "Modelo Campeón" (seleccionado en el Ejercicio 01) del entorno experimental a una simulación de producción: validar su robustez estadística, evaluar viabilidad técnica (latencia y memoria) y crear un script de inferencia reutilizable.

- **Metodología y hallazgos clave:**
    1. **Validación robusta:** validación cruzada estratificada (5 folds) sobre el modelo de 10 variables confirma estabilidad y que la selección no es aleatoria.
    2. **Escalabilidad (learning, scoring, storage):**
         - **Latencia (scoring):** inferencia < 1 ms, apto para entornos RTB.
         - **Almacenamiento:** artefacto final ≈ 2 KB, muy ligero.
    3. **Diagnóstico de calibración:** cálculo de Brier Score (MSE) y MAE sobre probabilidades. El modelo tiende a sobreestimar probabilidades por el rebalanceo, pero mantiene un ranking confiable, válido para priorización mediante umbrales altos.
    4. **Script de producción:** desarrollo de `src/predictor.py` con una clase modular `CTRPredictor` que carga artefactos (`.joblib`, `.json`) y realiza inferencia en nuevos datos.
    5. **Prueba con datos reales:** el sistema asignó ~84% de probabilidad a un usuario que hizo clic y ~26% a uno que no, validando el flujo de negocio.

- **Tecnologías:** Python scripting, `joblib`, `json`, `scikit-learn` (inferencia), Git.
- **Archivo principal:** `notebooks/02-Champion-Model-y-Produccion.ipynb`
- **Script generado:** `src/predictor.py`
