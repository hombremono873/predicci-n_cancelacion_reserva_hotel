"""Cálculo de la probabilidad de cancelación de una reserva y de su nivel de riesgo."""
import pandas as pd

from reserva_hotel.configuracion import RECOMENDACIONES, VALORES_FIJOS
from reserva_hotel.transformacion import transformar_reserva


def convertir_a_cantidad(respuesta: bool) -> int:
    """Convierte un sí o no en la cantidad 1 o 0; el indicador de la transformación queda igual que en el entrenamiento."""
    if respuesta:
        return 1
    return 0


def armar_reserva(campos: dict) -> pd.DataFrame:
    """Convierte los campos que ingresa el usuario en una fila con las columnas originales del dataset limpio."""
    fila = {
        "tipo_hotel": campos["tipo_hotel"],
        "dias_anticipacion": campos["dias_anticipacion"],
        "mes_llegada": campos["mes_llegada"],
        "dia_llegada": campos["dia_llegada"],
        "noches_fin_semana": campos["noches_fin_semana"],
        "noches_entre_semana": campos["noches_entre_semana"],
        "adultos": campos["adultos"],
        "regimen_comidas": campos["regimen_comidas"],
        "pais_origen": campos["pais_origen"],
        "segmento_mercado": campos["segmento_mercado"],
        "canal_distribucion": campos["canal_distribucion"],
        "cancelaciones_previas": convertir_a_cantidad(campos["tuvo_cancelaciones_previas"]),
        "reservas_previas_no_canceladas": convertir_a_cantidad(campos["tuvo_reservas_previas"]),
        "habitacion_reservada": campos["habitacion_reservada"],
        "cambios_reserva": campos["cambios_reserva"],
        "tipo_deposito": campos["tipo_deposito"],
        "agente": campos["agente"],
        "tipo_cliente": campos["tipo_cliente"],
        "tarifa_diaria_promedio": campos["tarifa_diaria_promedio"],
        "parqueaderos_solicitados": convertir_a_cantidad(campos["solicito_parqueadero"]),
        "solicitudes_especiales": campos["solicitudes_especiales"],
    }
    # Variables que el modelo no usa, pero que la transformación necesita para armar los indicadores
    for variable in VALORES_FIJOS:
        fila[variable] = VALORES_FIJOS[variable]
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
