## 📁 Estructura del Capítulo

```
chapter-02/
├── data/                   
│   ├── nyt1.csv … nyt31.csv       # Datos de NYT (31 días)
│   └── rollingsales_manhattan.xls # Ventas de Manhattan
├── notebook/                
│   ├── eda_nyt.ipynb              # EDA un día (Python + seaborn)
│   ├── eda_nyt.Rmd                # EDA un día (R + ggplot2)
│   ├── automate_nyt.ipynb         # EDA multidiario (Python)
│   ├── automate_nyt_analysis.Rmd  # EDA multidiario (R)
│   ├── manhattan_analysis.ipynb   # Limpieza & EDA Manhattan (Python)
│   └── realdirect_strategy.md     # Estrategia de datos RealDirect
└── README.md                      # Este archivo
```

## 📊 Resumen de Contenidos

### Exploración Estadística (NYT)

- **Un día**: `eda_nyt.ipynb` / `eda_nyt.Rmd`
- **Multidiario**: `automate_nyt.ipynb` / `automate_nyt_analysis.Rmd`

### Caso RealDirect

- **Documento de Estrategia**: `realdirect_strategy.md`

### Mercado Inmobiliario (Manhattan)

- **Carga, Limpieza y EDA**: `manhattan_analysis.ipynb`

## 📊 Análisis en R y Python: Enfoques Complementarios

Para este análisis exploratorio de los datos (EDA), se implementaron dos enfoques paralelos utilizando R (`ggplot2`) y Python (`seaborn`). Ambos entornos permiten explorar y visualizar datos de manera efectiva, pero cada uno tiene fortalezas distintas:

- **R con ggplot2**: Se destaca por su estética visual refinada y su sintaxis declarativa, lo que permite construir gráficos complejos de forma estructurada y con mínima configuración. Es ideal para análisis estadísticos profundos y presentaciones formales.

- **Python con seaborn**: Permite una integración más fluida con procesos de machine learning y pipelines de análisis, ofreciendo flexibilidad en la manipulación de datos y una curva de aprendizaje amigable para quienes ya programan en Python.

### Beneficios de Desarrollar Ambos Enfoques en Paralelo

- Refuerza la comprensión de los conceptos fundamentales del análisis exploratorio.
- Valida la consistencia del análisis independientemente del lenguaje.
- Fortalece el portafolio profesional al mostrar dominio en herramientas complementarias.

## 📌 Observaciones Preliminares

- Los usuarios "Invalid" (Age ≤ 0) muestran un CTR casi el doble que los "Valid".
- Su proporción varía del ~30% inicial a ~45% (picos días 15–30) y vuelve a ~30% al día 31.
- Esto explica el pico de CTR global (~2%) cuando "Invalid" aumenta, y su caída (~1.86%) al descender su proporción.
- Los usuarios mayores de 65 años muestran un CTR promedio más alto que otros grupos.
- Una gran proporción de usuarios tiene Age = 0 (grupo "Invalid"), lo que podría reflejar visitantes no registrados.
- La mayoría de los usuarios registrados no hacen clics, pero existen diferencias claras por edad y género en quienes sí lo hacen.

**Nota**: Se ha mantenido el grupo etario "Invalid" (usuarios con edad igual o menor a cero) en ambos lenguajes para asegurar comparabilidad y transparencia en el tratamiento de datos faltantes o incompletos.

**Nota**: Aquí encuentras tanto los análisis técnicos (notebooks y RMarkdown) como los documentos estratégicos.
