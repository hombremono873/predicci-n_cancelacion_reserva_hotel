"""Tarjeta con el resultado de la predicción."""
import streamlit as st

from reserva_hotel.configuracion import COLORES_RIESGO


def formatear_porcentaje(valor: float) -> str:
    """Escribe una proporción como porcentaje entero, por ejemplo 0,68 como 68 %."""
    return f"{valor * 100:.0f} %"


def mostrar_resultado(probabilidad: float, riesgo: dict[str, str], umbral: float, tasa_promedio: float) -> None:
    """Muestra la probabilidad de cancelación, el nivel de riesgo, la recomendación y cómo se define cada nivel."""
    color = COLORES_RIESGO[riesgo["nivel"]]
    promedio = formatear_porcentaje(tasa_promedio)
    limite_alto = formatear_porcentaje(umbral)

    with st.container(border=True):
        st.metric("Probabilidad de cancelación", formatear_porcentaje(probabilidad))
        st.progress(probabilidad)
        st.caption(
            f"De cada 100 reservas como esta, se esperaría que cancelen unas {probabilidad * 100:.0f}. "
            f"En el hotel cancelan en promedio {tasa_promedio * 100:.0f} de cada 100."
        )
        st.markdown(f"### :{color}[Riesgo {riesgo['nivel']}]")
        st.write(riesgo["recomendacion"])

    with st.container(border=True):
        st.markdown("**Cómo se define el riesgo**")
        st.markdown(
            f":green[**Bajo**]: menos de {promedio}, que es el promedio de cancelación del hotel.  \n"
            f":orange[**Medio**]: de {promedio} a {limite_alto}.  \n"
            f":red[**Alto**]: desde {limite_alto}, el umbral elegido en el menú lateral."
        )
