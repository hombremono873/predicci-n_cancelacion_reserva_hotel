"""Campos de entrada de la reserva, agrupados en sub-pestañas."""
from datetime import date

import streamlit as st

from reserva_hotel.agencias import GUIA_AGENCIAS
from reserva_hotel.configuracion import (
    ADULTOS_MAXIMOS, BEBES_MAXIMOS, CAMBIOS_MAXIMOS, CODIGOS_REGIMEN, DIAS_ANTICIPACION_MAXIMOS,
    DIAS_LISTA_ESPERA_MAXIMOS, EJEMPLOS, ETIQUETAS_CATEGORIAS, HISTORIAL_MAXIMO, NINOS_MAXIMOS,
    NOCHES_ENTRE_SEMANA_MAXIMAS, NOCHES_FIN_SEMANA_MAXIMAS, SOLICITUDES_MAXIMAS, TARIFA_MAXIMA,
    VARIABLE_DE_CADA_CAMPO,
)


def cargar_ejemplo(nombre_ejemplo: str) -> None:
    """Copia los valores de un ejemplo en los campos de la pantalla."""
    ejemplo = EJEMPLOS[nombre_ejemplo]
    for campo in ejemplo:
        valor = ejemplo[campo]
        if campo == "fecha_llegada":
            valor = date.fromisoformat(valor)
        st.session_state[campo] = valor


def cargar_ejemplo_elegido() -> None:
    """Carga el ejemplo que el usuario eligió en el menú lateral."""
    cargar_ejemplo(st.session_state["ejemplo"])


def se_muestra(campo: str, predictoras: list[str]) -> bool:
    """Indica si un campo se muestra: solo cuando el modelo usa la variable que se calcula con él."""
    return VARIABLE_DE_CADA_CAMPO[campo] in predictoras


def etiquetar(variable: str, categoria: str) -> str:
    """Devuelve la etiqueta en español de una categoría, o la categoría tal cual si no tiene etiqueta."""
    etiquetas = ETIQUETAS_CATEGORIAS.get(variable, {})
    if categoria in etiquetas:
        return etiquetas[categoria]
    return categoria


def etiquetar_hotel(categoria: str) -> str:
    """Etiqueta del tipo de hotel."""
    return etiquetar("tipo_hotel", categoria)


def etiquetar_regimen(categoria: str) -> str:
    """Etiqueta del régimen de comidas."""
    return etiquetar("regimen_comidas", categoria)


def etiquetar_segmento(categoria: str) -> str:
    """Etiqueta del segmento de mercado."""
    return etiquetar("segmento_mercado", categoria)


def etiquetar_canal(categoria: str) -> str:
    """Etiqueta del canal de distribución."""
    return etiquetar("canal_distribucion", categoria)


def etiquetar_cliente(categoria: str) -> str:
    """Etiqueta del tipo de cliente."""
    return etiquetar("tipo_cliente", categoria)


def etiquetar_deposito(categoria: str) -> str:
    """Etiqueta del tipo de depósito."""
    return etiquetar("tipo_deposito", categoria)


def etiquetar_pais(categoria: str) -> str:
    """Etiqueta del país: su nombre completo en español, o el código si el nombre no se conoce."""
    return etiquetar("pais_origen", categoria)


def etiquetar_habitacion(categoria: str) -> str:
    """Etiqueta del tipo de habitación: la letra y, entre paréntesis, qué tan común es y su tarifa típica."""
    return etiquetar("habitacion_reservada", categoria)


def etiquetar_agente(categoria: str) -> str:
    """Etiqueta de la agencia: su código y, entre paréntesis, qué tan común es y su tarifa típica."""
    if categoria == "Sin agente":
        nombre = "Sin agencia"
    else:
        nombre = f"Agencia {categoria}"
    if categoria in GUIA_AGENCIAS:
        return f"{nombre} ({GUIA_AGENCIAS[categoria]})"
    return nombre


def ordenar_agencias(agencias: list[str]) -> list[str]:
    """Ordena las agencias de la más común a la menos común; las que no tienen guía van al final."""
    ordenadas = []
    for agencia in GUIA_AGENCIAS:
        if agencia in agencias:
            ordenadas.append(agencia)
    for agencia in agencias:
        if agencia not in ordenadas:
            ordenadas.append(agencia)
    return ordenadas


def mostrar_llegada(predictoras: list[str], campos: dict) -> None:
    """Campos de la llegada y la estancia."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("fecha_llegada", predictoras):
            campos["fecha_llegada"] = st.date_input("Fecha de llegada", key="fecha_llegada", format="DD/MM/YYYY")
        if se_muestra("dias_anticipacion", predictoras):
            campos["dias_anticipacion"] = st.slider(
                "Días de anticipación", 0, DIAS_ANTICIPACION_MAXIMOS, key="dias_anticipacion",
                help="Días entre el momento de la reserva y la fecha de llegada.",
            )
    with derecha:
        if se_muestra("noches_fin_semana", predictoras):
            campos["noches_fin_semana"] = st.slider("Noches de fin de semana", 0, NOCHES_FIN_SEMANA_MAXIMAS, key="noches_fin_semana")
        if se_muestra("noches_entre_semana", predictoras):
            campos["noches_entre_semana"] = st.slider("Noches entre semana", 0, NOCHES_ENTRE_SEMANA_MAXIMAS, key="noches_entre_semana")


def mostrar_huespedes(predictoras: list[str], campos: dict) -> None:
    """Campos de los huéspedes y el régimen de comidas."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("adultos", predictoras):
            campos["adultos"] = st.number_input("Adultos", 1, ADULTOS_MAXIMOS, key="adultos")
        if se_muestra("ninos", predictoras):
            campos["ninos"] = st.number_input("Niños", 0, NINOS_MAXIMOS, key="ninos")
        if se_muestra("bebes", predictoras):
            campos["bebes"] = st.number_input("Bebés", 0, BEBES_MAXIMOS, key="bebes")
    with derecha:
        if se_muestra("regimen_comidas", predictoras):
            campos["regimen_comidas"] = st.radio(
                "Régimen de comidas", list(CODIGOS_REGIMEN), key="regimen_comidas", format_func=etiquetar_regimen,
            )


def mostrar_canal(predictoras: list[str], opciones: dict[str, list[str]], campos: dict) -> None:
    """Campos del hotel, el canal de venta y el cliente."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("tipo_hotel", predictoras):
            campos["tipo_hotel"] = st.radio(
                "Tipo de hotel", opciones["tipo_hotel"], key="tipo_hotel",
                format_func=etiquetar_hotel, horizontal=True,
            )
        if se_muestra("segmento_mercado", predictoras):
            campos["segmento_mercado"] = st.selectbox(
                "Segmento de mercado", opciones["segmento_mercado"], key="segmento_mercado", format_func=etiquetar_segmento,
            )
        if se_muestra("canal_distribucion", predictoras):
            campos["canal_distribucion"] = st.selectbox(
                "Canal de distribución", opciones["canal_distribucion"], key="canal_distribucion", format_func=etiquetar_canal,
            )
    with derecha:
        if se_muestra("pais_origen", predictoras):
            # Países en orden alfabético de su nombre en español
            paises = sorted(opciones["pais_origen"], key=etiquetar_pais)
            campos["pais_origen"] = st.selectbox(
                "País de origen", paises, key="pais_origen", format_func=etiquetar_pais,
                help="Escriba el nombre del país para buscarlo.",
            )
        if se_muestra("tipo_cliente", predictoras):
            campos["tipo_cliente"] = st.selectbox(
                "Tipo de cliente", opciones["tipo_cliente"], key="tipo_cliente", format_func=etiquetar_cliente,
            )
        if se_muestra("tipo_deposito", predictoras):
            campos["tipo_deposito"] = st.selectbox(
                "Tipo de depósito", opciones["tipo_deposito"], key="tipo_deposito", format_func=etiquetar_deposito,
            )

    # La agencia y la habitación van a lo ancho, para que su guía se lea completa
    if se_muestra("agente", predictoras):
        campos["agente"] = st.selectbox(
            "Agencia de viajes", ordenar_agencias(opciones["agente"]), key="agente", format_func=etiquetar_agente,
            help="Cada agencia se identifica con un código. Como guía se muestra qué tan común es y su tarifa "
                 "típica por noche; están ordenadas de la más común a la menos común. Escriba el código para buscarla.",
        )
    if se_muestra("habitacion_reservada", predictoras):
        campos["habitacion_reservada"] = st.selectbox(
            "Tipo de habitación reservada", opciones["habitacion_reservada"], key="habitacion_reservada",
            format_func=etiquetar_habitacion,
            help="El hotel identifica cada tipo de habitación con una letra. Como guía se muestra qué tan "
                 "común es y su tarifa típica por noche.",
        )


def mostrar_historial(predictoras: list[str], campos: dict) -> None:
    """Campos del historial del cliente, la tarifa y las solicitudes."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("cancelaciones_previas", predictoras):
            campos["cancelaciones_previas"] = st.number_input(
                "Cancelaciones previas del cliente", 0, HISTORIAL_MAXIMO, key="cancelaciones_previas",
            )
        if se_muestra("reservas_previas_no_canceladas", predictoras):
            campos["reservas_previas_no_canceladas"] = st.number_input(
                "Reservas previas cumplidas", 0, HISTORIAL_MAXIMO, key="reservas_previas_no_canceladas",
            )
        if se_muestra("cambios_reserva", predictoras):
            campos["cambios_reserva"] = st.number_input("Cambios en la reserva", 0, CAMBIOS_MAXIMOS, key="cambios_reserva")
        if se_muestra("dias_lista_espera", predictoras):
            campos["dias_lista_espera"] = st.number_input(
                "Días en lista de espera", 0, DIAS_LISTA_ESPERA_MAXIMOS, key="dias_lista_espera",
            )
    with derecha:
        if se_muestra("tarifa_diaria_promedio", predictoras):
            campos["tarifa_diaria_promedio"] = st.slider("Tarifa por noche", 0, TARIFA_MAXIMA, key="tarifa_diaria_promedio")
        if se_muestra("solicitudes_especiales", predictoras):
            campos["solicitudes_especiales"] = st.slider(
                "Solicitudes especiales", 0, SOLICITUDES_MAXIMAS, key="solicitudes_especiales",
                help="Por ejemplo, cama doble o piso alto.",
            )
        if se_muestra("parqueaderos_solicitados", predictoras):
            pide_parqueadero = st.toggle("Solicita parqueadero", value=campos["parqueaderos_solicitados"] > 0)
            if pide_parqueadero:
                campos["parqueaderos_solicitados"] = 1
            else:
                campos["parqueaderos_solicitados"] = 0
        if se_muestra("cliente_recurrente", predictoras):
            campos["cliente_recurrente"] = int(st.toggle("Cliente recurrente", value=campos["cliente_recurrente"] == 1))
        if se_muestra("empresa", predictoras):
            campos["empresa"] = st.toggle("Reserva a nombre de una empresa", key="empresa")


def mostrar_campos(predictoras: list[str], opciones: dict[str, list[str]]) -> dict:
    """Muestra los campos de la reserva en cuatro sub-pestañas y devuelve los valores ingresados."""
    # Se parte de los valores actuales; los campos que el modelo no usa conservan el valor del ejemplo
    campos = {}
    for campo in VARIABLE_DE_CADA_CAMPO:
        campos[campo] = st.session_state[campo]

    llegada, huespedes, canal, historial = st.tabs(["Llegada", "Huéspedes", "Canal y cliente", "Historial"])
    with llegada:
        mostrar_llegada(predictoras, campos)
    with huespedes:
        mostrar_huespedes(predictoras, campos)
    with canal:
        mostrar_canal(predictoras, opciones, campos)
    with historial:
        mostrar_historial(predictoras, campos)
    return campos
