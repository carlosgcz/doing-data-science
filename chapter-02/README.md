## 📁 Estructura del capítulo
```
chapter-02/
├── data/                   # Archivos CSV: nyt1.csv a nyt31.csv
├── notebook/               # Scripts y notebooks en Python y/o R
│   ├── eda_nyt.ipynb       # Análisis EDA en Python
│   └── eda_nyt.Rmd         # Análisis EDA en R
└── README.md               # Descripción del capítulo y avances
```
### 📊 Análisis en R y Python: Enfoques complementarios

Para este análisis exploratorio de los datos (EDA), se implementaron dos enfoques paralelos utilizando R (`ggplot2`) y Python (`seaborn`). Ambos entornos permiten explorar y visualizar datos de manera efectiva, pero cada uno tiene fortalezas distintas:

- **R con ggplot2**: se destaca por su estética visual refinada y su sintaxis declarativa, lo que permite construir gráficos complejos en forma estructurada y con mínima configuración. Ideal para análisis estadísticos profundos y presentaciones formales.

- **Python con seaborn**: permite una integración más fluida con procesos de machine learning y pipelines de análisis, ofreciendo flexibilidad en manipulación de datos y una curva de aprendizaje amigable para quienes ya programan en Python.

Al desarrollar ambos enfoques en paralelo:
- Se refuerza la comprensión de los conceptos fundamentales del análisis exploratorio.
- Se valida la consistencia del análisis independientemente del lenguaje.
- Se fortalece el portafolio profesional al mostrar dominio en herramientas complementarias.

### 📌 Observaciones preliminares

- Los usuarios mayores de 65 años muestran un CTR promedio más alto que otros grupos.
- Una gran proporción de usuarios tiene `Age = 0` (grupo "Invalid"), lo que podría reflejar visitantes no registrados.
- La mayoría de los usuarios registrados no hacen clics, pero existen diferencias claras por edad y género en quienes sí lo hacen.

> 🧠 Nota: Se ha mantenido el grupo etario `"Invalid"` (usuarios con edad igual o menor a cero) en ambos lenguajes para asegurar comparabilidad y transparencia en el tratamiento de datos faltantes o incompletos.

