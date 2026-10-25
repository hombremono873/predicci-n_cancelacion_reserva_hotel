"""Tarjeta con el resultado de la predicción."""
import streamlit as st

from reserva_hotel.configuracion import COLORES_RIESGO


def formatear_porcentaje(valor: float) -> str:
    """Escribe una proporción como porcentaje entero, por ejemplo 0,68 como 68 %."""
    return f"{valor * 100:.0f} %"


def mostrar_resultado(probabilidad: float, riesgo: dict[str, str], umbral: float, tasa_promedio: float) -> None:
    """Muestra la probabilidad de cancelación, el nivel de riesgo y la recomendación."""
    diferencia = (probabilidad - tasa_promedio) * 100
    color = COLORES_RIESGO[riesgo["nivel"]]

    with st.container(border=True):
        st.metric(
            "Probabilidad de cancelación",
            formatear_porcentaje(probabilidad),
            delta=f"{diferencia:+.0f} puntos frente al promedio",
            delta_color="inverse",
        )
        st.progress(probabilidad)
        st.markdown(f"### :{color}[Riesgo {riesgo['nivel']}]")
        st.write(riesgo["recomendacion"])
        st.caption(
            f"Promedio de cancelación del hotel: {formatear_porcentaje(tasa_promedio)}. "
            f"Umbral de riesgo alto: {formatear_porcentaje(umbral)}."
        )
