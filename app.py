"""Aplicación Streamlit: riesgo de cancelación de reservas hoteleras."""
import streamlit as st

from reserva_hotel.configuracion import (
    EJEMPLO_INICIAL, EJEMPLOS, PASO_UMBRAL, RUTA_MODELO, TASA_CANCELACION_DATOS, UMBRAL_MAXIMO, UMBRAL_MINIMO,
)
from reserva_hotel.interfaz.entradas import cargar_ejemplo, cargar_ejemplo_elegido, mostrar_campos
from reserva_hotel.interfaz.explicacion import mostrar_explicacion
from reserva_hotel.interfaz.portada import mostrar_portada, volver_a_la_portada
from reserva_hotel.interfaz.salidas import mostrar_resultado
from reserva_hotel.persistencia import (
    cargar_modelo, existe_modelo, obtener_nombre_modelo, obtener_opciones, version_compatible,
)
from reserva_hotel.prediccion import calcular_probabilidad, clasificar_riesgo


@st.cache_resource
def obtener_modelo() -> dict:
    """Carga el modelo una sola vez y lo reutiliza en cada interacción."""
    return cargar_modelo(RUTA_MODELO)


def mostrar_menu_lateral(paquete: dict) -> float:
    """Muestra el menú lateral y devuelve el umbral de riesgo alto elegido."""
    with st.sidebar:
        st.markdown("### Riesgo de cancelación")
        st.caption("Complete los datos de la reserva para estimar su probabilidad de cancelación.")

        st.selectbox(
            "Cargar un ejemplo", list(EJEMPLOS), key="ejemplo", on_change=cargar_ejemplo_elegido,
            help="Llena todos los campos con una reserva típica de riesgo bajo, medio o alto.",
        )
        st.caption("Llena el formulario con una reserva de muestra. Después puede cambiar cualquier dato.")

        umbral_porcentaje = st.slider(
            "Umbral de riesgo alto", UMBRAL_MINIMO, UMBRAL_MAXIMO, step=PASO_UMBRAL, key="umbral", format="%d %%",
            help="Desde esta probabilidad, una reserva se considera de riesgo alto.",
        )
        st.caption(
            "Desde este porcentaje la reserva se marca como riesgo alto. Un valor más bajo detecta más "
            "cancelaciones, pero también da más falsas alarmas."
        )

        st.divider()
        st.markdown("**Modelo**")
        st.caption(f"{obtener_nombre_modelo(paquete)}  \n{len(paquete['predictoras'])} variables")

        st.divider()
        st.button("Ver créditos", type="tertiary", on_click=volver_a_la_portada)
    return umbral_porcentaje / 100


def iniciar_estado(paquete: dict) -> None:
    """Carga el ejemplo inicial y el umbral del modelo la primera vez que se abre la aplicación."""
    if "ejemplo" not in st.session_state:
        st.session_state["ejemplo"] = EJEMPLO_INICIAL
        st.session_state["umbral"] = round(paquete["umbral"] * 100)
        cargar_ejemplo(EJEMPLO_INICIAL)


def main() -> None:
    """Arma la página: título, menú lateral y las pestañas de predicción y explicación."""
    st.set_page_config(page_title="Riesgo de Cancelación de Reservas", page_icon=":material/hotel:", layout="wide")

    # Al abrir la aplicación se muestra primero la portada con los créditos
    if "portada_vista" not in st.session_state:
        mostrar_portada()
        return

    st.title("Riesgo de Cancelación de Reservas")
    st.caption("Estima la probabilidad de que una reserva hotelera sea cancelada.")

    if not existe_modelo(RUTA_MODELO):
        st.error(
            "No se encontró el modelo. Ejecute el notebook en Colab y copie "
            "modelo_cancelaciones.joblib en la carpeta modelos del proyecto."
        )
        st.stop()

    # Un modelo guardado con otra versión de scikit-learn puede no cargar
    try:
        paquete = obtener_modelo()
    except Exception as error:
        st.error(
            "No se pudo cargar el modelo. Lo más probable es que se haya entrenado con otra versión de "
            "scikit-learn: instale las versiones de requirements.txt o vuelva a exportar el modelo desde Colab."
        )
        st.caption(f"Detalle: {error}")
        st.stop()
    if not version_compatible(paquete):
        st.warning(
            f"El modelo se entrenó con scikit-learn {paquete['version_sklearn']}. "
            "Instale esa misma versión para evitar resultados incorrectos."
        )

    iniciar_estado(paquete)
    umbral = mostrar_menu_lateral(paquete)

    prediccion, explicacion = st.tabs([
        ":material/edit_note: Predicción",
        ":material/info: Cómo funciona",
    ])

    with prediccion:
        datos_reserva, resultado = st.columns([3, 2], gap="large")
        with datos_reserva:
            st.caption(
                f"Los campos vienen llenos con el ejemplo **{st.session_state['ejemplo']}** del menú lateral. "
                "Cambie los datos que quiera y el resultado se actualiza solo."
            )
            campos =mostrar_campos(paquete["predictoras"], obtener_opciones(paquete))
        with resultado:
            probabilidad = calcular_probabilidad(paquete, campos)
            riesgo = clasificar_riesgo(probabilidad, umbral, TASA_CANCELACION_DATOS)
            mostrar_resultado(probabilidad, riesgo, umbral, TASA_CANCELACION_DATOS)

    with explicacion:
        mostrar_explicacion(TASA_CANCELACION_DATOS)


if __name__ == "__main__":
    main()
