# Módulo: Capítulo 4 - Filtros de Spam, Naive Bayes y Manejo de Datos

## Descripción

Este módulo se centra en la clasificación de texto, utilizando el algoritmo Naive Bayes como pilar fundamental. A través de los ejercicios de este capítulo de *Doing Data Science*, se profundiza en el ciclo de vida completo de un proyecto de Procesamiento de Lenguaje Natural (PLN), desde el preprocesamiento y la limpieza de texto crudo (*data wrangling*) hasta la construcción, optimización y validación de un modelo predictivo.

---

## Contenido Detallado

### **Exercise 01: Filtro de Spam con Naive Bayes (Dataset Enron)**

- **Objetivo:** Implementar desde cero un clasificador de spam para el dataset de correos de Enron, superando el ejemplo base del libro. El enfoque principal está en un riguroso manejo de datos (*wrangling*) y en la optimización de hiperparámetros para maximizar la precisión del modelo.
- **Metodología:**
    1. **Pipeline de Datos:** Se construye un proceso para cargar, limpiar (eliminar metadatos, puntuación), normalizar (minúsculas) y reducir la dimensionalidad del texto mediante *stemming*.
    2. **Clasificador Naive Bayes:** Se desarrolla una función propia que implementa la lógica del algoritmo, calculando las probabilidades condicionales para clasificar nuevos correos.
    3. **Optimización y Validación:** Se realiza un ajuste iterativo del parámetro de suavizado (alpha) y se refina la lista de *stop words*. El rendimiento se mide en un conjunto de prueba separado.
    4. **Resultado:** Se alcanza una **precisión del 93.8%** en el conjunto de prueba, demostrando la alta efectividad del método optimizado.
- **Tecnologías:** R, R Markdown, `tm`, `SnowballC`.
- **Notebook:** [`enron_spam_filter.Rmd`](./enron_spam_filter.Rmd)

---
