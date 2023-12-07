"""
Módulo para realizar un Análisis Exploratorio de Datos (EDA) básico en un archivo CSV.
"""

import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def execute_analysis(file_name: str, normalize_cols=True,
                     check_duplicates=True, show_summary_flag=True) -> pd.DataFrame:
    """
    Ejecuta un análisis exploratorio de datos en un archivo CSV.

    :param file_name: Nombre del archivo CSV a leer.
    :param normalize_cols: Booleano, si se normalizan los nombres de columnas.
    :param check_duplicates: Booleano, si se verifica y elimina duplicados.
    :param show_summary_flag: Booleano, si se muestra un resumen del DataFrame.
    :return: DataFrame de pandas o None en caso de error.
    """
    current_dir = os.getcwd()

    # Intenta leer desde el directorio actual, luego 'datasets', y 'notebooks'
    for folder in ['', 'datasets', 'notebooks']:
        try:
            data_frame = pd.read_csv(os.path.join(
                current_dir, folder, file_name))
            break
        except FileNotFoundError:
            continue
        except pd.errors.EmptyDataError:
            print(f"Error: Archivo {file_name} vacío.")
            return None
        except pd.errors.ParserError as e:
            print(f"Error al parsear el archivo {file_name}: {e}")
            return None

    if data_frame is None or data_frame.empty:
        print("No hay datos para análisis.")
        return None

    if normalize_cols:
        data_frame = normalize_column_names(data_frame)

    if check_duplicates:
        data_frame = check_for_duplicates(data_frame)
        if data_frame.empty:
            print("Datos vacíos tras eliminar duplicados.")
            return None

    if show_summary_flag:
        show_summary(data_frame)

    return data_frame


def normalize_column_names(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas de un DataFrame a snake_case.

    :param data_frame: DataFrame de pandas.
    :return: DataFrame con nombres de columnas normalizados.
    """
    # *********** Corregir: Está colocando doble guión bajo ***********
    data_frame.columns = [re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower().replace(' ', '_').replace('__', '_')
                          for col in data_frame.columns]
    return data_frame


def check_for_duplicates(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Verifica y elimina filas duplicadas en un DataFrame.

    :param data_frame: DataFrame de pandas.
    :return: DataFrame sin duplicados.
    """
    if data_frame.duplicated().sum() > 0:
        print("Duplicados encontrados. Eliminando...")
        data_frame.drop_duplicates(inplace=True)
    return data_frame


def show_summary(data_frame: pd.DataFrame):
    """
    Muestra un resumen del DataFrame.

    :param data_frame: DataFrame de pandas.
    """
    print("Primeras 5 filas:")
    print(data_frame.head())
    print("\nÚltimas 5 filas:")
    print(data_frame.tail())
    print("\nMuestra aleatoria de 5 filas:")
    print(data_frame.sample(5))

    print("\nInformación del DataFrame:")
    print(data_frame.info())

    print("\nEstadísticas Descriptivas:")
    print(data_frame.describe())

    print("\nValores Faltantes:")
    print(data_frame.isnull().sum())

    print("\nHistogramas para Variables Numéricas:")
    data_frame.hist(bins=15, figsize=(15, 10))
    plt.show()

    if data_frame.select_dtypes(include=[np.number]).shape[1] > 1:
        print("\nMapa de Calor de Correlación:")
        sns.heatmap(data_frame.corr(), annot=True)
        plt.show()

    print("\nAnálisis de Variables Categóricas:")
    for column in data_frame.select_dtypes(include=['object']).columns:
        print(f"\nDistribución de la variable {column}:")
        print(data_frame[column].value_counts())
        sns.countplot(y=column, data=data_frame)
        plt.show()


if __name__ == "__main__":
    execute_analysis('tu_archivo.csv', normalize_cols=True,
                     check_duplicates=False, show_summary_flag=True)
