# datadivecsv: Análisis Exploratorio de Datos para CSV

El módulo datadivecsv proporciona una herramienta sencilla y eficaz para realizar un análisis exploratorio básico de datos contenidos en archivos CSV. Este módulo es ideal para obtener una rápida comprensión de los datos, especialmente útil en las etapas iniciales de cualquier proyecto de análisis de datos.

## Características

- Lectura de Archivos CSV: Capacidad para leer archivos CSV desde el directorio actual o subdirectorios específicos (datasets, notebooks).
- Normalización de Nombres de Columnas: Opción para convertir nombres de columnas a snake_case, facilitando el manejo de los datos.
- Verificación y Eliminación de Duplicados: Chequea y elimina filas duplicadas en el conjunto de datos para asegurar la precisión del análisis.
- Resumen del DataFrame: Proporciona un resumen exhaustivo del DataFrame, incluyendo las primeras y últimas filas, una muestra aleatoria de filas, información del DataFrame, estadísticas descriptivas, valores faltantes, y más.
- Visualización de Datos: Genera histogramas para variables numéricas y mapas de calor de correlación, además de análisis de variables categóricas.

## Uso

Para utilizar datadivecsv, simplemente importa la función execute_analysis y pásale el nombre del archivo CSV que deseas analizar. Aquí tienes un ejemplo básico de uso:

```py
from datadivecsv import execute_analysis

df = execute_analysis('tu_archivo.csv', normalize_cols=True, check_duplicates=True, show_summary_flag=True)
```

**Parámetros de execute_analysis**

- `file_name`: Nombre del archivo CSV a analizar.
- `normalize_cols` (opcional): Booleano para normalizar los nombres de las columnas a snake_case (por defecto True).
- `check_duplicates` (opcional): Booleano para verificar y eliminar duplicados (por defecto True).
- `show_summary_flag` (opcional): Booleano para mostrar un resumen del DataFrame (por defecto True).

## Instalación

Puedes instalar este paquete usando pip:

```bash
pip install datadivecsv
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, revisa las `issues` en GitHub para ver cómo puedes contribuir.

## Licencia

Este proyecto está bajo la Licencia MIT.
