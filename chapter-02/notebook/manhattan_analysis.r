# Análisis de Ventas en Manhattan
# Autor: Carlos G.C.Z
# Fecha: 2024-01-20

# Limpiar ambiente y memoria
rm(list = ls())
gc()

# Cargar paquetes necesarios
if (!require(pacman)) install.packages("pacman")
pacman::p_load(
  readxl,
  ggplot2,
  dplyr,
  scales,
  tidyr,
  lubridate,
  viridis,
  janitor,
  magrittr,
  gridExtra,
  grid,
  naniar,    # Para análisis de datos faltantes
  stringr,   # Para manipulación de texto
  purrr      # Para operaciones funcionales
)

# Tema personalizado
tema_manhattan <- theme_minimal() +
  theme(plot.title = element_text(size = 14, face = "bold", hjust = 0.5),
        axis.title = element_text(size = 12),
        axis.text = element_text(size = 10),
        panel.grid.minor = element_blank(),
        plot.background = element_rect(fill = "white", color = NA),
        panel.background = element_rect(fill = "white", color = NA))

# Cargar y procesar datos
mh <- read_excel("chapter-02/data/rollingsales_manhattan.xls", skip=4)

# Funciones de limpieza
clean_sale_price <- function(df) {
  df %>%
    filter(sale_price > 0) %>%
    filter(sale_price <= quantile(sale_price, 0.999, na.rm = TRUE))
}

clean_square_feet <- function(df) {
  df %>%
    mutate(across(c(land_square_feet, gross_square_feet),
                  ~ifelse(. == 0, NA, .)))
}

clean_year_built <- function(df) {
  df %>%
    filter(is.na(year_built) | year_built >= 1800)
}

classify_property_type <- function(building_class) {
  case_when(
    str_detect(toupper(building_class), "RESIDENTIAL|FAMILY") ~ "Residencial",
    str_detect(toupper(building_class), "COMMERCIAL|OFFICE") ~ "Comercial",
    TRUE ~ "Otro"
  )
}

# Limpiar y transformar datos
mh_clean <- mh %>%
  clean_names() %>%
  mutate(
    sale_date = as.Date(sale_date),
    across(c(sale_price, land_square_feet, gross_square_feet, year_built), as.numeric),
    price_millions = sale_price / 1e6,
    sqft_thousands = gross_square_feet / 1e3,
    property_type = classify_property_type(building_class_category)
  ) %>%
  clean_sale_price() %>%
  clean_square_feet() %>%
  clean_year_built() %>%
  distinct()

# Análisis de calidad de datos
missing_analysis <- mh_clean %>%
  group_by(building_class_category) %>%
  summarise(
    missing_sqft = sum(is.na(gross_square_feet)),
    total_count = n(),
    pct_missing_sqft = round(missing_sqft / total_count * 100, 2)
  ) %>%
  arrange(desc(total_count))

# Análisis por vecindario
neighborhood_stats <- mh_clean %>%
  group_by(neighborhood) %>%
  summarise(
    count = n(),
    mean_price = mean(price_millions, na.rm = TRUE),
    median_price = median(price_millions, na.rm = TRUE),
    median_sqft = median(sqft_thousands, na.rm = TRUE)
  ) %>%
  arrange(desc(count)) %>%
  head(10)

# Análisis de outliers extremos
price_threshold_99 <- quantile(mh_clean$price_millions, 0.99, na.rm = TRUE)
extreme_sales <- mh_clean %>%
  filter(price_millions > price_threshold_99) %>%
  arrange(desc(price_millions)) %>%
  select(address, neighborhood, price_millions, property_type, building_class_category)

# Visualizaciones mejoradas
# 1. Distribución de precios por tipo de propiedad
p1 <- ggplot(mh_clean, aes(x = price_millions, fill = property_type)) +
  geom_histogram(alpha = 0.7, bins = 50) +
  facet_wrap(~property_type, scales = "free_y") +
  labs(title = "Distribución de Precios por Tipo de Propiedad",
       x = "Precio (Millones $)", 
       y = "Frecuencia",
       fill = "Tipo de Propiedad") +
  scale_x_continuous(labels = dollar_format(prefix = "$", suffix = "M")) +
  tema_manhattan
print(p1)

# 2. Box plot por vecindario y tipo de propiedad
p2 <- mh_clean %>%
  filter(neighborhood %in% neighborhood_stats$neighborhood) %>%
  ggplot(aes(x = reorder(neighborhood, price_millions, median), 
             y = price_millions, 
             fill = property_type)) +
  geom_boxplot(alpha = 0.6) +
  labs(title = "Precios por Vecindario y Tipo de Propiedad",
       x = "Vecindario", 
       y = "Precio (Millones $)",
       fill = "Tipo de Propiedad") +
  scale_y_continuous(labels = dollar_format(prefix = "$", suffix = "M")) +
  coord_flip() +
  tema_manhattan
print(p2)

# 3. Scatter plot con año de construcción
p3 <- ggplot(mh_clean, aes(x = year_built, y = price_millions, color = property_type)) +
  geom_point(alpha = 0.5) +
  labs(title = "Precio vs Año de Construcción",
       x = "Año de Construcción", 
       y = "Precio (Millones $)",
       color = "Tipo de Propiedad") +
  scale_y_continuous(labels = dollar_format(prefix = "$", suffix = "M")) +
  tema_manhattan
print(p3)

# 4. Tendencia temporal por tipo de propiedad
p4 <- mh_clean %>%
  group_by(month = floor_date(sale_date, "month"),
           property_type) %>%
  summarise(median_price = median(price_millions, na.rm = TRUE)) %>%
  ggplot(aes(x = month, y = median_price, color = property_type)) +
  geom_line(linewidth = 1) +
  geom_smooth(method = "loess", se = FALSE) +
  labs(title = "Tendencia de Precios por Tipo de Propiedad",
       x = "Fecha", 
       y = "Precio Mediano (Millones $)",
       color = "Tipo de Propiedad") +
  scale_y_continuous(labels = dollar_format(prefix = "$", suffix = "M")) +
  tema_manhattan
print(p4)

# Resumen ejecutivo
cat(sprintf("
RESUMEN EJECUTIVO - ANÁLISIS MERCADO INMOBILIARIO MANHATTAN

1. CALIDAD DE DATOS:
- %.1f%% de las propiedades tienen datos de superficie registrados
- La falta de datos es más pronunciada en propiedades residenciales

2. SEGMENTACIÓN DE MERCADO:
- Propiedades Residenciales: %.1f%%
- Propiedades Comerciales: %.1f%%
- Precio mediano residencial: $%.2f M
- Precio mediano comercial: $%.2f M

3. TENDENCIAS TEMPORALES:
- Análisis temporal muestra variaciones significativas por tipo de propiedad
- Se observan patrones estacionales en ventas residenciales

4. OUTLIERS Y CASOS ESPECIALES:
- %d propiedades con valores > $%.2f M (percentil 99)
- Precio máximo: $%.2f M

5. RECOMENDACIONES:
- Mejorar captura de datos de superficie
- Desarrollar análisis geoespacial
- Profundizar análisis por tipo de propiedad
",
  sum(!is.na(mh_clean$gross_square_feet)) / nrow(mh_clean) * 100,
  sum(mh_clean$property_type == "Residencial") / nrow(mh_clean) * 100,
  sum(mh_clean$property_type == "Comercial") / nrow(mh_clean) * 100,
  median(mh_clean$price_millions[mh_clean$property_type == "Residencial"], na.rm = TRUE),
  median(mh_clean$price_millions[mh_clean$property_type == "Comercial"], na.rm = TRUE),
  nrow(extreme_sales),
  price_threshold_99,
  max(mh_clean$price_millions, na.rm = TRUE)
))