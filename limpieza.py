"""Limpieza y transformación del dataset: duplicados, fugas, valores imposibles, imputación, indicadores y codificación."""
import os

import numpy as np
import pandas as pd

from constantes import (
    CATEGORIA_MAS_FRECUENTE, CODIGOS_MES, CODIGOS_REGIMEN, INDICADORES_BINARIOS, MAXIMO_ADULTOS,
    TARIFA_MAXIMA_VALIDA, TASA_CANCELACION_MAXIMA, TASA_CANCELACION_MINIMA, VARIABLES_CON_LOGARITMO,
    VARIABLE_OBJETIVO,
)


# Paso 17. Eliminación de filas duplicadas
def informar_filas_eliminadas(datos_antes: pd.DataFrame, datos_despues: pd.DataFrame) -> None:
    """Muestra cuántas filas se eliminaron en un paso y cuántas quedan."""
    print("Filas eliminadas:", len(datos_antes) - len(datos_despues))
    print("Filas restantes:", len(datos_despues))


def eliminar_duplicados(datos: pd.DataFrame) -> pd.DataFrame:
    """Elimina las filas repetidas y conserva la primera aparición de cada una."""
    datos_sin_repetidas = datos.drop_duplicates()
    return datos_sin_repetidas.reset_index(drop=True)


# Paso 18. Eliminación de columnas con fuga de datos o sin aporte
def eliminar_columnas(datos: pd.DataFrame, columnas: dict[str, str]) -> pd.DataFrame:
    """Elimina las columnas indicadas y muestra el motivo de cada una."""
    for columna in columnas:
        print(f"{columna}: {columnas[columna]}")
    return datos.drop(columns=list(columnas))


# Paso 19. Eliminación de reservas con valores imposibles
def eliminar_filas_invalidas(datos: pd.DataFrame) -> pd.DataFrame:
    """Elimina las reservas con tarifa imposible, sin huéspedes o sin noches."""
    total_huespedes = datos["adultos"] + datos["ninos"].fillna(0) + datos["bebes"]
    total_noches = datos["noches_fin_semana"] + datos["noches_entre_semana"]

    # Una reserva es válida si cumple las tres condiciones a la vez
    tarifa_valida = datos["tarifa_diaria_promedio"].between(0, TARIFA_MAXIMA_VALIDA)
    tiene_huespedes = total_huespedes > 0
    tiene_noches = total_noches > 0
    filas_validas = tarifa_valida & tiene_huespedes & tiene_noches

    return datos[filas_validas].reset_index(drop=True)


# Paso 20. Imputación de valores nulos
def imputar_nulos(datos: pd.DataFrame) -> pd.DataFrame:
    """Rellena los nulos de niños, país de origen y agente."""
    datos = datos.copy()
    datos["ninos"] = datos["ninos"].fillna(0).astype(int)
    datos["pais_origen"] = datos["pais_origen"].fillna("Desconocido")

    # Los códigos de agente son identificadores: se pasan a texto sin decimales (9.0 pasa a ser 9)
    datos["agente"] = datos["agente"].astype("Int64").astype("string")
    datos["agente"] = datos["agente"].fillna("Sin agente")
    return datos


# Paso 21. Corrección de categorías indefinidas
def corregir_categorias(datos: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza la categoría Undefined en el régimen de comidas, el canal y el segmento."""
    datos = datos.copy()
    datos["regimen_comidas"] = datos["regimen_comidas"].replace("Undefined", "SC")
    for variable in CATEGORIA_MAS_FRECUENTE:
        datos[variable] = datos[variable].replace("Undefined", CATEGORIA_MAS_FRECUENTE[variable])
    return datos


# Paso 22. Creación de indicadores binarios
def crear_indicadores(datos: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza las variables con más del 90 % de ceros por indicadores de 0 y 1, y crea tiene_hijos y tiene_empresa."""
    datos = datos.copy()
    for original in INDICADORES_BINARIOS:
        indicador = INDICADORES_BINARIOS[original]
        datos[indicador] = (datos[original] > 0).astype(int)
    datos["tiene_hijos"] = ((datos["ninos"] + datos["bebes"]) > 0).astype(int)
    datos["tiene_empresa"] = datos["empresa"].notna().astype(int)

    # Se eliminan las columnas originales que quedaron reemplazadas por los indicadores
    columnas_reemplazadas = list(INDICADORES_BINARIOS)
    columnas_reemplazadas.append("ninos")
    columnas_reemplazadas.append("bebes")
    columnas_reemplazadas.append("empresa")
    return datos.drop(columns=columnas_reemplazadas)


# Paso 23. Transformación de colas largas y recorte de adultos
def transformar_colas_largas(datos: pd.DataFrame) -> pd.DataFrame:
    """Aplica logaritmo a las noches, raíz cuadrada a la anticipación y un máximo a los adultos."""
    datos = datos.copy()
    for variable in VARIABLES_CON_LOGARITMO:
        datos[variable] = np.log1p(datos[variable])
    datos["dias_anticipacion"] = np.sqrt(datos["dias_anticipacion"])
    datos["adultos"] = datos["adultos"].clip(upper=MAXIMO_ADULTOS)
    return datos


# Paso 24. Codificación de las variables ordinales
def codificar_ordinales(datos: pd.DataFrame) -> pd.DataFrame:
    """Convierte el mes y el régimen de comidas en números que respetan su orden natural."""
    datos = datos.copy()
    datos["mes_llegada"] = datos["mes_llegada"].map(CODIGOS_MES)
    datos["regimen_comidas"] = datos["regimen_comidas"].map(CODIGOS_REGIMEN)
    return datos


# Paso 25. Validación del dataset limpio
def validar_limpieza(datos: pd.DataFrame) -> None:
    """Detiene el flujo si el dataset limpio tiene nulos o una tasa de cancelación fuera de lo esperado."""
    nulos = datos.isna().sum().sum()
    if nulos > 0:
        raise ValueError(f"El dataset limpio tiene {nulos} valores nulos; revise los pasos de transformación.")

    tasa = datos[VARIABLE_OBJETIVO].mean()
    if tasa < TASA_CANCELACION_MINIMA or tasa > TASA_CANCELACION_MAXIMA:
        raise ValueError(f"La tasa de cancelación ({tasa:.1%}) está fuera del rango esperado.")

    print("Filas:", len(datos))
    print("Columnas:", datos.shape[1])
    print("Valores nulos:", nulos)
    print(f"Tasa de cancelación: {tasa:.1%}")


# Paso 26. Guardado del dataset limpio
def guardar_datos(datos: pd.DataFrame, ruta: str) -> None:
    """Guarda el dataset en un archivo CSV sin la columna de índice."""
    datos.to_csv(ruta, index=False)
    print("Dataset guardado en:", os.path.abspath(ruta))
