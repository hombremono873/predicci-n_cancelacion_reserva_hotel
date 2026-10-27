"""Pestaña con la explicación breve del modelo."""
import streamlit as st


def mostrar_explicacion(tasa_cancelacion: float) -> None:
    """Explica qué datos usa el modelo, cómo leer el resultado y cuáles son sus limitaciones."""
    tasa = f"{tasa_cancelacion * 100:.1f}".replace(".", ",")
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        st.markdown("#### Qué hace")
        st.write(
            "Estima la probabilidad de que una reserva sea cancelada antes de la llegada, a partir de "
            "la anticipación, la estancia, el canal de venta, el cliente y su historial."
        )
        st.markdown("#### Con qué datos aprendió")
        st.write(
            f"Con 86.637 reservas de dos hoteles de Portugal entre 2015 y 2017, sin duplicados ni valores "
            f"imposibles. El {tasa} % de esas reservas se canceló."
        )
        st.markdown("#### Cómo leer el resultado")
        st.write(
            "**Riesgo alto**: la probabilidad llega al umbral elegido en el menú lateral. "
            "**Riesgo medio**: está entre el promedio del hotel y el umbral. "
            "**Riesgo bajo**: está por debajo del promedio."
        )
    with derecha:
        st.markdown("#### Qué significan las métricas")
        st.write(
            "**Precisión**: de las reservas marcadas como canceladas, cuántas lo son. "
            "**Recall**: de las reservas canceladas, cuántas detecta el modelo. "
            "**F1**: equilibrio entre las dos. **AUC**: qué tan bien ordena las reservas por riesgo."
        )
        st.markdown("#### Limitaciones")
        st.write(
            "Los datos son de dos hoteles y de hace varios años; los patrones de otros hoteles o de hoy "
            "pueden ser distintos. El modelo indica un riesgo, no una certeza: debe apoyar la decisión, "
            "no reemplazarla."
        )
