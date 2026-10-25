"""Cálculo de la probabilidad de cancelación de una reserva y de su nivel de riesgo."""
import numpy as np
import pandas as pd

from reserva_hotel.configuracion import MESES_EN_INGLES, RECOMENDACIONES
from reserva_hotel.transformacion import transformar_reserva


def armar_reserva(campos: dict) -> pd.DataFrame:
    """Convierte los campos que ingresa el usuario en una fila con las columnas originales del dataset limpio."""
    fecha = campos["fecha_llegada"]
    if campos["empresa"]:
        empresa = 1
    else:
        empresa = np.nan

    fila = {
        "tipo_hotel": campos["tipo_hotel"],
        "dias_anticipacion": campos["dias_anticipacion"],
        "mes_llegada": MESES_EN_INGLES[fecha.month - 1],
        "semana_llegada": fecha.isocalendar()[1],
        "dia_llegada": fecha.day,
        "noches_fin_semana": campos["noches_fin_semana"],
        "noches_entre_semana": campos["noches_entre_semana"],
        "adultos": campos["adultos"],
        "ninos": campos["ninos"],
        "bebes": campos["bebes"],
        "regimen_comidas": campos["regimen_comidas"],
        "pais_origen": campos["pais_origen"],
        "segmento_mercado": campos["segmento_mercado"],
        "canal_distribucion": campos["canal_distribucion"],
        "cliente_recurrente": campos["cliente_recurrente"],
        "cancelaciones_previas": campos["cancelaciones_previas"],
        "reservas_previas_no_canceladas": campos["reservas_previas_no_canceladas"],
        "habitacion_reservada": campos["habitacion_reservada"],
        "cambios_reserva": campos["cambios_reserva"],
        "tipo_deposito": campos["tipo_deposito"],
        "agente": campos["agente"],
        "empresa": empresa,
        "dias_lista_espera": campos["dias_lista_espera"],
        "tipo_cliente": campos["tipo_cliente"],
        "tarifa_diaria_promedio": campos["tarifa_diaria_promedio"],
        "parqueaderos_solicitados": campos["parqueaderos_solicitados"],
        "solicitudes_especiales": campos["solicitudes_especiales"],
    }
    return pd.DataFrame([fila])


def calcular_probabilidad(paquete: dict, campos: dict) -> float:
    """Transforma la reserva igual que en el entrenamiento y devuelve su probabilidad de cancelación."""
    reserva = armar_reserva(campos)
    reserva_transformada = transformar_reserva(reserva)
    predictoras = reserva_transformada[paquete["predictoras"]]
    probabilidades = paquete["modelo"].predict_proba(predictoras)
    return float(probabilidades[0, 1])   # fila de la reserva, columna de la clase "cancelada"


def clasificar_riesgo(probabilidad: float, umbral: float, tasa_promedio: float) -> dict[str, str]:
    """Clasifica el riesgo: alto desde el umbral, medio entre el promedio del hotel y el umbral, bajo por debajo."""
    if probabilidad >= umbral:
        nivel = "alto"
    elif probabilidad >= tasa_promedio:
        nivel = "medio"
    else:
        nivel = "bajo"
    return {"nivel": nivel, "recomendacion": RECOMENDACIONES[nivel]}
