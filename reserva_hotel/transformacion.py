"""Transformaciones de una reserva al formato que espera el modelo; son las mismas del notebook."""
import numpy as np
import pandas as pd

from reserva_hotel.configuracion import (
    CODIGOS_MES, CODIGOS_REGIMEN, INDICADORES_BINARIOS, MAXIMO_ADULTOS, VARIABLES_CON_LOGARITMO,
)


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


def transformar_colas_largas(datos: pd.DataFrame) -> pd.DataFrame:
    """Aplica logaritmo a las noches, raíz cuadrada a la anticipación y un máximo a los adultos."""
    datos = datos.copy()
    for variable in VARIABLES_CON_LOGARITMO:
        datos[variable] = np.log1p(datos[variable])
    datos["dias_anticipacion"] = np.sqrt(datos["dias_anticipacion"])
    datos["adultos"] = datos["adultos"].clip(upper=MAXIMO_ADULTOS)
    return datos


def codificar_ordinales(datos: pd.DataFrame) -> pd.DataFrame:
    """Convierte el mes y el régimen de comidas en números que respetan su orden natural."""
    datos = datos.copy()
    datos["mes_llegada"] = datos["mes_llegada"].map(CODIGOS_MES)
    datos["regimen_comidas"] = datos["regimen_comidas"].map(CODIGOS_REGIMEN)
    return datos


def transformar_reserva(reserva: pd.DataFrame) -> pd.DataFrame:
    """Aplica a una reserva las mismas transformaciones que se usaron para entrenar el modelo."""
    reserva_con_indicadores = crear_indicadores(reserva)
    reserva_transformada = transformar_colas_largas(reserva_con_indicadores)
    return codificar_ordinales(reserva_transformada)
