"""Campos de entrada de la reserva: uno por predictora del modelo, agrupados en sub-pestañas."""
import streamlit as st

from reserva_hotel.agencias import GUIA_AGENCIAS
from reserva_hotel.configuracion import (
    ADULTOS_MAXIMOS, ADULTOS_MINIMOS, AYUDAS_CAMPOS, CAMBIOS_MAXIMOS, CAMPOS, CODIGOS_REGIMEN,
    COMBINACIONES_SEGMENTO_CANAL, DIAS_ANTICIPACION_MAXIMOS, DIAS_POR_MES, EJEMPLOS, ETIQUETAS_CAMPOS,
    ETIQUETAS_CATEGORIAS, MESES_EN_INGLES, NOCHES_ENTRE_SEMANA_MAXIMAS, NOCHES_FIN_SEMANA_MAXIMAS,
    SOLICITUDES_MAXIMAS, TARIFA_MAXIMA,
)


def cargar_ejemplo(nombre_ejemplo: str) -> None:
    """Copia los valores de un ejemplo en los campos de la pantalla."""
    ejemplo = EJEMPLOS[nombre_ejemplo]
    for campo in ejemplo:
        st.session_state[campo] = ejemplo[campo]


def cargar_ejemplo_elegido() -> None:
    """Carga el ejemplo que el usuario eligió en el menú lateral."""
    cargar_ejemplo(st.session_state["ejemplo"])


def ajustar_dia() -> None:
    """Al cambiar el mes, baja el día al último del mes si el elegido no existe (por ejemplo, 31 de abril)."""
    ultimo_dia = DIAS_POR_MES[st.session_state["mes_llegada"]]
    if st.session_state["dia_llegada"] > ultimo_dia:
        st.session_state["dia_llegada"] = ultimo_dia


def canales_del_segmento(segmento: str, canales_del_modelo: list[str]) -> list[str]:
    """Devuelve los canales que aparecen en los datos con el segmento y que el modelo conoce."""
    canales = []
    for canal in COMBINACIONES_SEGMENTO_CANAL[segmento]:
        if canal in canales_del_modelo:
            canales.append(canal)
    return canales


def ajustar_canal() -> None:
    """Al cambiar el segmento, si el canal elegido no aparece con él en los datos, pasa al canal más común."""
    canales = COMBINACIONES_SEGMENTO_CANAL[st.session_state["segmento_mercado"]]
    if st.session_state["canal_distribucion"] not in canales:
        st.session_state["canal_distribucion"] = canales[0]


def se_muestra(campo: str, predictoras: list[str]) -> bool:
    """Indica si un campo se muestra: solo cuando su variable es una predictora del modelo."""
    return campo in predictoras


def etiquetar(variable: str, categoria: str) -> str:
    """Devuelve la etiqueta en español de una categoría, o la categoría tal cual si no tiene etiqueta."""
    etiquetas = ETIQUETAS_CATEGORIAS.get(variable, {})
    if categoria in etiquetas:
        return etiquetas[categoria]
    return categoria


def etiquetar_mes(categoria: str) -> str:
    """Nombre del mes en español."""
    return etiquetar("mes_llegada", categoria)


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
    """Etiqueta del tipo de habitación: la letra y, entre paréntesis, qué tan común es."""
    return etiquetar("habitacion_reservada", categoria)


def etiquetar_agente(categoria: str) -> str:
    """Etiqueta del agente: su código y, entre paréntesis, qué tan común es en las reservas."""
    if categoria == "Sin agente":
        nombre = "Sin agente"
    else:
        nombre = f"Agente {categoria}"
    if categoria not in GUIA_AGENCIAS:
        return nombre
    # El primero de la guía es el más frecuente
    if categoria == list(GUIA_AGENCIAS)[0]:
        return f"{nombre} (el más frecuente: {GUIA_AGENCIAS[categoria]})"
    return f"{nombre} ({GUIA_AGENCIAS[categoria]})"


def ordenar_agentes(agentes: list[str]) -> list[str]:
    """Ordena los agentes del más común al menos común; los que no tienen guía van al final."""
    ordenados = []
    for agente in GUIA_AGENCIAS:
        if agente in agentes:
            ordenados.append(agente)
    for agente in agentes:
        if agente not in ordenados:
            ordenados.append(agente)
    return ordenados


def ordenar_tipos_cliente(tipos: list[str]) -> list[str]:
    """Ordena los tipos de cliente como en sus etiquetas: del más común al menos común en los datos."""
    ordenados = []
    for tipo in ETIQUETAS_CATEGORIAS["tipo_cliente"]:
        if tipo in tipos:
            ordenados.append(tipo)
    for tipo in tipos:
        if tipo not in ordenados:
            ordenados.append(tipo)
    return ordenados


def ordenar_paises(paises: list[str]) -> list[str]:
    """Ordena los países alfabéticamente por su nombre en español."""
    return sorted(paises, key=etiquetar_pais)


def mostrar_llegada(predictoras: list[str], campos: dict) -> None:
    """Campos de la fecha de llegada y la estancia."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("mes_llegada", predictoras):
            campos["mes_llegada"] = st.selectbox(
                ETIQUETAS_CAMPOS["mes_llegada"], MESES_EN_INGLES, key="mes_llegada", format_func=etiquetar_mes,
                on_change=ajustar_dia, help=AYUDAS_CAMPOS["mes_llegada"],
            )
        if se_muestra("dia_llegada", predictoras):
            # El último día depende del mes elegido
            campos["dia_llegada"] = st.number_input(
                ETIQUETAS_CAMPOS["dia_llegada"], 1, DIAS_POR_MES[campos["mes_llegada"]], key="dia_llegada",
                help=AYUDAS_CAMPOS["dia_llegada"],
            )
        if se_muestra("dias_anticipacion", predictoras):
            campos["dias_anticipacion"] = st.slider(
                ETIQUETAS_CAMPOS["dias_anticipacion"], 0, DIAS_ANTICIPACION_MAXIMOS, key="dias_anticipacion",
                help=AYUDAS_CAMPOS["dias_anticipacion"],
            )
    with derecha:
        if se_muestra("noches_fin_semana", predictoras):
            campos["noches_fin_semana"] = st.slider(
                ETIQUETAS_CAMPOS["noches_fin_semana"], 0, NOCHES_FIN_SEMANA_MAXIMAS, key="noches_fin_semana",
                help=AYUDAS_CAMPOS["noches_fin_semana"],
            )
        if se_muestra("noches_entre_semana", predictoras):
            campos["noches_entre_semana"] = st.slider(
                ETIQUETAS_CAMPOS["noches_entre_semana"], 0, NOCHES_ENTRE_SEMANA_MAXIMAS, key="noches_entre_semana",
                help=AYUDAS_CAMPOS["noches_entre_semana"],
            )


def mostrar_reserva(predictoras: list[str], opciones: dict[str, list[str]], campos: dict) -> None:
    """Campos del hotel, la habitación, los huéspedes, la tarifa y los servicios."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("tipo_hotel", predictoras):
            campos["tipo_hotel"] = st.radio(
                ETIQUETAS_CAMPOS["tipo_hotel"], opciones["tipo_hotel"], key="tipo_hotel",
                format_func=etiquetar_hotel, horizontal=True, help=AYUDAS_CAMPOS["tipo_hotel"],
            )
        if se_muestra("habitacion_reservada", predictoras):
            campos["habitacion_reservada"] = st.selectbox(
                ETIQUETAS_CAMPOS["habitacion_reservada"], opciones["habitacion_reservada"],
                key="habitacion_reservada", format_func=etiquetar_habitacion,
                help=AYUDAS_CAMPOS["habitacion_reservada"],
            )
        if se_muestra("regimen_comidas", predictoras):
            campos["regimen_comidas"] = st.radio(
                ETIQUETAS_CAMPOS["regimen_comidas"], list(CODIGOS_REGIMEN), key="regimen_comidas",
                format_func=etiquetar_regimen, help=AYUDAS_CAMPOS["regimen_comidas"],
            )
        if se_muestra("adultos", predictoras):
            campos["adultos"] = st.number_input(
                ETIQUETAS_CAMPOS["adultos"], ADULTOS_MINIMOS, ADULTOS_MAXIMOS, key="adultos",
                help=AYUDAS_CAMPOS["adultos"],
            )
        if se_muestra("tipo_deposito", predictoras):
            campos["tipo_deposito"] = st.selectbox(
                ETIQUETAS_CAMPOS["tipo_deposito"], opciones["tipo_deposito"], key="tipo_deposito",
                format_func=etiquetar_deposito, help=AYUDAS_CAMPOS["tipo_deposito"],
            )
    with derecha:
        if se_muestra("tarifa_diaria_promedio", predictoras):
            campos["tarifa_diaria_promedio"] = st.slider(
                ETIQUETAS_CAMPOS["tarifa_diaria_promedio"], 0, TARIFA_MAXIMA, key="tarifa_diaria_promedio",
                format="%d €", help=AYUDAS_CAMPOS["tarifa_diaria_promedio"],
            )
        if se_muestra("cambios_reserva", predictoras):
            campos["cambios_reserva"] = st.number_input(
                ETIQUETAS_CAMPOS["cambios_reserva"], 0, CAMBIOS_MAXIMOS, key="cambios_reserva",
                help=AYUDAS_CAMPOS["cambios_reserva"],
            )
        if se_muestra("solicitudes_especiales", predictoras):
            campos["solicitudes_especiales"] = st.slider(
                ETIQUETAS_CAMPOS["solicitudes_especiales"], 0, SOLICITUDES_MAXIMAS, key="solicitudes_especiales",
                help=AYUDAS_CAMPOS["solicitudes_especiales"],
            )
        if se_muestra("solicito_parqueadero", predictoras):
            campos["solicito_parqueadero"] = st.toggle(
                ETIQUETAS_CAMPOS["solicito_parqueadero"], key="solicito_parqueadero",
                help=AYUDAS_CAMPOS["solicito_parqueadero"],
            )


def mostrar_canal(predictoras: list[str], opciones: dict[str, list[str]], campos: dict) -> None:
    """Campos del canal de venta: segmento, canal y agente."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("segmento_mercado", predictoras):
            campos["segmento_mercado"] = st.selectbox(
                ETIQUETAS_CAMPOS["segmento_mercado"], opciones["segmento_mercado"], key="segmento_mercado",
                format_func=etiquetar_segmento, on_change=ajustar_canal, help=AYUDAS_CAMPOS["segmento_mercado"],
            )
    with derecha:
        if se_muestra("canal_distribucion", predictoras):
            # Solo se ofrecen los canales que aparecen en los datos con el segmento elegido
            canales = canales_del_segmento(campos["segmento_mercado"], opciones["canal_distribucion"])
            campos["canal_distribucion"] = st.selectbox(
                ETIQUETAS_CAMPOS["canal_distribucion"], canales, key="canal_distribucion",
                format_func=etiquetar_canal, help=AYUDAS_CAMPOS["canal_distribucion"],
            )

    # El agente va a lo ancho, para que su guía se lea completa
    if se_muestra("agente", predictoras):
        campos["agente"] = st.selectbox(
            ETIQUETAS_CAMPOS["agente"], ordenar_agentes(opciones["agente"]), key="agente",
            format_func=etiquetar_agente, help=AYUDAS_CAMPOS["agente"],
        )


def mostrar_cliente(predictoras: list[str], opciones: dict[str, list[str]], campos: dict) -> None:
    """Campos del cliente y su historial con el hotel."""
    izquierda, derecha = st.columns(2, gap="large")
    with izquierda:
        if se_muestra("pais_origen", predictoras):
            campos["pais_origen"] = st.selectbox(
                ETIQUETAS_CAMPOS["pais_origen"], ordenar_paises(opciones["pais_origen"]), key="pais_origen",
                format_func=etiquetar_pais, help=AYUDAS_CAMPOS["pais_origen"],
            )
        if se_muestra("tipo_cliente", predictoras):
            campos["tipo_cliente"] = st.selectbox(
                ETIQUETAS_CAMPOS["tipo_cliente"], ordenar_tipos_cliente(opciones["tipo_cliente"]), key="tipo_cliente",
                format_func=etiquetar_cliente, help=AYUDAS_CAMPOS["tipo_cliente"],
            )
    with derecha:
        if se_muestra("tuvo_cancelaciones_previas", predictoras):
            campos["tuvo_cancelaciones_previas"] = st.toggle(
                ETIQUETAS_CAMPOS["tuvo_cancelaciones_previas"], key="tuvo_cancelaciones_previas",
                help=AYUDAS_CAMPOS["tuvo_cancelaciones_previas"],
            )
        if se_muestra("tuvo_reservas_previas", predictoras):
            campos["tuvo_reservas_previas"] = st.toggle(
                ETIQUETAS_CAMPOS["tuvo_reservas_previas"], key="tuvo_reservas_previas",
                help=AYUDAS_CAMPOS["tuvo_reservas_previas"],
            )


def mostrar_campos(predictoras: list[str], opciones: dict[str, list[str]]) -> dict:
    """Muestra los campos de la reserva en cuatro sub-pestañas y devuelve los valores ingresados."""
    # Se parte de los valores actuales de la pantalla (los del ejemplo o los que cambió el usuario)
    campos = {}
    for campo in CAMPOS:
        campos[campo] = st.session_state[campo]

    llegada, reserva, canal, cliente = st.tabs(["Llegada y estancia", "Reserva", "Canal de venta", "Cliente"])
    with llegada:
        mostrar_llegada(predictoras, campos)
    with reserva:
        mostrar_reserva(predictoras, opciones, campos)
    with canal:
        mostrar_canal(predictoras, opciones, campos)
    with cliente:
        mostrar_cliente(predictoras, opciones, campos)
    return campos
