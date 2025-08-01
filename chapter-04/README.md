# Módulo: Capítulo 4 - Naive Bayes y Clasificación de Texto

## Descripción

Este módulo explora la clasificación de texto a través de dos proyectos prácticos que demuestran el ciclo de vida completo de un proyecto de Procesamiento de Lenguaje Natural (PLN). Se abordan desde los fundamentos teóricos del algoritmo Naive Bayes hasta su implementación, optimización y evaluación en contextos reales.

El capítulo progresa desde un clásico filtro de spam binomial implementado en R, hasta un clasificador multi-clase más complejo en Python, incluyendo la recolección de datos robusta desde una API externa.

---

## Contenido Detallado

### **Ejercicio 01: Filtro de Spam con Naive Bayes (Dataset Enron)**

- **Objetivo:** Implementar desde cero un clasificador de spam para el dataset de correos de Enron, superando el ejemplo base del libro. El enfoque principal está en un riguroso manejo de datos (*wrangling*) y en la optimización de hiperparámetros.
- **Metodología:**
    1. **Pipeline de Datos en R:** Se construye un proceso para cargar, limpiar, normalizar y tokenizar el texto.
    2. **Clasificador Naive Bayes:** Se desarrolla una función propia que implementa la lógica del algoritmo, calculando las probabilidades condicionales para clasificar nuevos correos.
    3. **Optimización y Validación:** Se realiza un ajuste iterativo del parámetro de suavizado (alpha) y se refina la lista de *stop words* para medir el rendimiento en un conjunto de prueba.
- **Tecnologías:** R, R Markdown, `tm`, `SnowballC`, `tidytext`.
- **Archivo:** [`enron_spam_filter.Rmd`](./enron_spam_filter.Rmd)

---

### **Ejercicio 02: Clasificador de Artículos del NYT (Python)**

- **Objetivo:** Implementar un pipeline completo en Python para clasificar artículos del New York Times en 5 categorías distintas (`News`, `Business`, `Culture`, `Science`, `Sports`), desde la recolección de datos hasta la optimización de un modelo multi-clase.
- **Metodología:**
    1. **Recolección de Datos Robusta (Python Script):** Se desarrolló un script para consumir la API del NYT, implementando una estrategia de "rendimiento controlado" para obtener un dataset balanceado. El script incluye manejo de errores, gestión de límites de API y guardado seguro ante interrupciones.
    2. **Pipeline de Datos y Modelo (Jupyter Notebook):** Se implementó un clasificador **Bernoulli Naive Bayes desde cero**. El pipeline incluye preprocesamiento de texto avanzado con `spaCy` y la creación de matrices de características dispersas (`scipy.sparse`) para máxima eficiencia.
    3. **Optimización de Hiperparámetros:** Se realizó un ajuste sistemático de `alpha` (suavizado) y `VOCAB_SIZE` (tamaño del vocabulario). Este proceso fue clave para **elevar la precisión del modelo desde un 53.34% hasta un 75.42%**.
    4. **Análisis y Conclusiones:** El notebook finaliza con un análisis profundo de los resultados, incluyendo palabras informativas, análisis de errores y un resumen ejecutivo profesional con fórmulas en formato LaTeX.
- **Tecnologías:** Python, Jupyter, Pandas, `spaCy`, `scikit-learn`, `matplotlib`.
- **Archivos:**
  - Script de recolección: [`fetch_articles.py`](./fetch_articles.py)
  - Notebook de análisis: [`naive_bayes_classifier.ipynb`](./naive_bayes_classifier.ipynb)
