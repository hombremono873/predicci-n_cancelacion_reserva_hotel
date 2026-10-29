"""Constantes de la aplicación: rutas, transformaciones, campos, rangos, ejemplos, etiquetas y colores."""
import os

from reserva_hotel.paises import NOMBRES_PAISES

# Rutas
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_MODELO = os.path.join(CARPETA_PROYECTO, "modelos", "modelo_cancelaciones.joblib")

# Tasa de cancelación de los datos limpios del notebook (Paso 24): separa el riesgo bajo del medio
TASA_CANCELACION_DATOS = 0.277

# Nombre en español de cada tipo de modelo
NOMBRES_MODELOS = {
    "LogisticRegression": "Regresión logística",
    "RandomForestClassifier": "Random Forest",
    "HistGradientBoostingClassifier": "Gradient Boosting",
}

# Transformaciones: deben ser las mismas del notebook (pasos 21 a 23)
INDICADORES_BINARIOS = {
    "cancelaciones_previas": "tuvo_cancelaciones_previas",
    "reservas_previas_no_canceladas": "tuvo_reservas_previas",
    "dias_lista_espera": "estuvo_en_lista_espera",
    "parqueaderos_solicitados": "solicito_parqueadero",
}
VARIABLES_CON_LOGARITMO = ["noches_entre_semana", "noches_fin_semana"]
MAXIMO_ADULTOS = 4

MESES_EN_INGLES = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
]
CODIGOS_MES = {}
numero_mes = 1
for mes in MESES_EN_INGLES:
    CODIGOS_MES[mes] = numero_mes
    numero_mes = numero_mes + 1

CODIGOS_REGIMEN = {"SC": 0, "BB": 1, "HB": 2, "FB": 3}

# Campos del formulario: uno por cada predictora del modelo ganador, con el mismo nombre
CAMPOS = [
    "mes_llegada", "dia_llegada", "dias_anticipacion", "noches_fin_semana", "noches_entre_semana",
    "tipo_hotel", "habitacion_reservada", "regimen_comidas", "adultos", "tarifa_diaria_promedio",
    "tipo_deposito", "cambios_reserva", "solicitudes_especiales", "solicito_parqueadero",
    "segmento_mercado", "canal_distribucion", "agente",
    "pais_origen", "tipo_cliente", "tuvo_cancelaciones_previas", "tuvo_reservas_previas",
]

# Variables del dataset que el modelo ganador no usa. La transformación las necesita para armar
# la fila de la reserva, pero no cambian la probabilidad; se dejan en el valor más común (cero).
VALORES_FIJOS = {"ninos": 0, "bebes": 0, "cliente_recurrente": 0, "dias_lista_espera": 0, "empresa": None}

# Nombre visible de cada campo: la variable escrita de forma legible
ETIQUETAS_CAMPOS = {
    "mes_llegada": "Mes de llegada",
    "dia_llegada": "Día de llegada",
    "dias_anticipacion": "Días de anticipación",
    "noches_fin_semana": "Noches de fin de semana",
    "noches_entre_semana": "Noches entre semana",
    "tipo_hotel": "Tipo de hotel",
    "habitacion_reservada": "Habitación reservada",
    "regimen_comidas": "Régimen de comidas",
    "adultos": "Adultos",
    "tarifa_diaria_promedio": "Tarifa diaria promedio",
    "tipo_deposito": "Tipo de depósito",
    "cambios_reserva": "Cambios de la reserva",
    "solicitudes_especiales": "Solicitudes especiales",
    "solicito_parqueadero": "Solicitó parqueadero",
    "segmento_mercado": "Segmento de mercado",
    "canal_distribucion": "Canal de distribución",
    "agente": "Agente",
    "pais_origen": "País de origen",
    "tipo_cliente": "Tipo de cliente",
    "tuvo_cancelaciones_previas": "Tuvo cancelaciones previas",
    "tuvo_reservas_previas": "Tuvo reservas previas",
}

# Texto de ayuda de cada campo: empieza con el nombre de la variable y luego la explica
AYUDAS_CAMPOS = {
    "mes_llegada": "Variable: mes_llegada. Mes en que el huésped llega al hotel.",
    "dia_llegada": "Variable: dia_llegada. Día del mes en que el huésped llega al hotel.",
    "dias_anticipacion": "Variable: dias_anticipacion. Días entre el momento de la reserva y la fecha de llegada.",
    "noches_fin_semana": "Variable: noches_fin_semana. Noches de sábado o domingo de la estancia.",
    "noches_entre_semana": "Variable: noches_entre_semana. Noches de lunes a viernes de la estancia.",
    "tipo_hotel": "Variable: tipo_hotel. Hotel urbano o resort.",
    "habitacion_reservada": (
        "Variable: habitacion_reservada. El hotel identifica cada tipo de habitación con una letra anónima; "
        "como guía se muestra qué tan común es."
    ),
    "regimen_comidas": "Variable: regimen_comidas. Plan de alimentación contratado, de menor a mayor servicio.",
    "adultos": (
        "Variable: adultos. Número de adultos de la reserva. El modelo trata igual las reservas de 4 o más "
        "adultos, porque en los datos casi no hay reservas con más."
    ),
    "tarifa_diaria_promedio": (
        "Variable: tarifa_diaria_promedio. Precio promedio por noche, en euros, como en los datos de "
        "entrenamiento. El máximo es la tarifa más alta de los datos limpios."
    ),
    "tipo_deposito": (
        "Variable: tipo_deposito. Sin depósito, reembolsable o no reembolsable (el cliente pierde el pago "
        "si cancela). En los datos, el 94,7 % de las reservas no reembolsables se canceló: casi todas eran de "
        "clientes de Portugal, sobre todo reservas de grupo y de agencias hechas con mucha anticipación. Por "
        "eso el modelo da un riesgo muy alto con esta opción, aunque no sea lo lógico para una reserva individual."
    ),
    "cambios_reserva": "Variable: cambios_reserva. Modificaciones hechas a la reserva antes de la llegada.",
    "solicitudes_especiales": "Variable: solicitudes_especiales. Peticiones del cliente, como cama doble o piso alto.",
    "solicito_parqueadero": "Variable: solicito_parqueadero. Si el cliente pidió al menos un espacio de parqueo.",
    "segmento_mercado": (
        "Variable: segmento_mercado. Cómo se vendió la reserva: agencia en línea, agencia tradicional u "
        "operador, grupo, corporativo o directo."
    ),
    "canal_distribucion": (
        "Variable: canal_distribucion. Medio por el que llegó la reserva: agencia u operador (TA/TO), "
        "directo, corporativo o sistema global de reservas (GDS). Solo se ofrecen los canales que aparecen "
        "en los datos con el segmento elegido."
    ),
    "agente": (
        "Variable: agente. Código anónimo de la agencia de viajes intermediaria. Elija Sin agente si el "
        "cliente reservó directamente. El modelo trata como un solo grupo los agentes con menos del 1 % de "
        "las reservas. Escriba el código para buscarlo."
    ),
    "pais_origen": (
        "Variable: pais_origen. País del cliente; el modelo trata como un solo grupo los países con menos "
        "del 1 % de las reservas. Escriba el nombre para buscarlo."
    ),
    "tipo_cliente": "Variable: tipo_cliente. Transitorio, transitorio asociado, grupo o contrato.",
    "tuvo_cancelaciones_previas": (
        "Variable: tuvo_cancelaciones_previas. Si el cliente canceló alguna reserva antes. El modelo solo "
        "distingue entre sí y no."
    ),
    "tuvo_reservas_previas": (
        "Variable: tuvo_reservas_previas. Si el cliente tiene alguna reserva anterior que no canceló. El "
        "modelo solo distingue entre sí y no."
    ),
}

# Rangos de los campos numéricos, tomados de los datos limpios del notebook (86.637 reservas)
DIAS_ANTICIPACION_MAXIMOS = 709
NOCHES_FIN_SEMANA_MAXIMAS = 19
NOCHES_ENTRE_SEMANA_MAXIMAS = 50
ADULTOS_MINIMOS = 1
ADULTOS_MAXIMOS = 4
CAMBIOS_MAXIMOS = 18
TARIFA_MAXIMA = 510
SOLICITUDES_MAXIMAS = 5

# Último día de cada mes en los datos (febrero llega a 29 porque 2016 fue bisiesto)
DIAS_POR_MES = {
    "January": 31, "February": 29, "March": 31, "April": 30, "May": 31, "June": 30,
    "July": 31, "August": 31, "September": 30, "October": 31, "November": 30, "December": 31,
}

# Canales que aparecen en los datos limpios con cada segmento, del más al menos frecuente.
# Las combinaciones que no están aquí no existen en los datos y la aplicación no las ofrece.
COMBINACIONES_SEGMENTO_CANAL = {
    "Aviation": ["Corporate", "TA/TO"],
    "Complementary": ["Direct", "Corporate", "TA/TO"],
    "Corporate": ["Corporate", "TA/TO", "Direct"],
    "Direct": ["Direct", "TA/TO", "Corporate", "GDS"],
    "Groups": ["TA/TO", "Corporate", "Direct"],
    "Offline TA/TO": ["TA/TO", "Corporate", "GDS", "Direct"],
    "Online TA": ["TA/TO", "GDS", "Direct", "Corporate"],
}

# Ejemplos: reservas reales de los datos limpios cuya probabilidad cae en el nivel de su nombre
EJEMPLOS = {
    "Riesgo bajo": {
        "mes_llegada": "May", "dia_llegada": 8, "dias_anticipacion": 2, "noches_fin_semana": 2,
        "noches_entre_semana": 0, "tipo_hotel": "City Hotel", "habitacion_reservada": "D",
        "regimen_comidas": "BB", "adultos": 2, "tarifa_diaria_promedio": 118, "tipo_deposito": "No Deposit",
        "cambios_reserva": 0, "solicitudes_especiales": 1, "solicito_parqueadero": False,
        "segmento_mercado": "Online TA", "canal_distribucion": "TA/TO", "agente": "9",
        "pais_origen": "FRA", "tipo_cliente": "Transient", "tuvo_cancelaciones_previas": False,
        "tuvo_reservas_previas": False,
    },
    "Riesgo medio": {
        "mes_llegada": "October", "dia_llegada": 17, "dias_anticipacion": 27, "noches_fin_semana": 1,
        "noches_entre_semana": 2, "tipo_hotel": "City Hotel", "habitacion_reservada": "A",
        "regimen_comidas": "HB", "adultos": 2, "tarifa_diaria_promedio": 177, "tipo_deposito": "No Deposit",
        "cambios_reserva": 0, "solicitudes_especiales": 2, "solicito_parqueadero": False,
        "segmento_mercado": "Online TA", "canal_distribucion": "TA/TO", "agente": "9",
        "pais_origen": "NLD", "tipo_cliente": "Transient", "tuvo_cancelaciones_previas": False,
        "tuvo_reservas_previas": False,
    },
    "Riesgo alto": {
        "mes_llegada": "September", "dia_llegada": 19, "dias_anticipacion": 36, "noches_fin_semana": 2,
        "noches_entre_semana": 2, "tipo_hotel": "Resort Hotel", "habitacion_reservada": "C",
        "regimen_comidas": "HB", "adultos": 2, "tarifa_diaria_promedio": 162, "tipo_deposito": "No Deposit",
        "cambios_reserva": 0, "solicitudes_especiales": 1, "solicito_parqueadero": False,
        "segmento_mercado": "Online TA", "canal_distribucion": "TA/TO", "agente": "242",
        "pais_origen": "PRT", "tipo_cliente": "Transient", "tuvo_cancelaciones_previas": False,
        "tuvo_reservas_previas": False,
    },
}
EJEMPLO_INICIAL = "Riesgo medio"

# Etiquetas en español de las categorías que se muestran en las listas
ETIQUETAS_CATEGORIAS = {
    "mes_llegada": {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre",
    },
    "tipo_hotel": {"City Hotel": "Urbano", "Resort Hotel": "Resort"},
    "regimen_comidas": {
        "SC": "Sin comidas", "BB": "Solo desayuno", "HB": "Media pensión", "FB": "Pensión completa",
    },
    "segmento_mercado": {
        "Online TA": "Agencia en línea", "Offline TA/TO": "Agencia tradicional u operador",
        "Groups": "Grupos", "Direct": "Directo", "Corporate": "Corporativo",
        "Complementary": "Cortesía", "Aviation": "Aerolínea",
    },
    "canal_distribucion": {
        "TA/TO": "Agencia u operador (TA/TO)", "Direct": "Directo",
        "Corporate": "Corporativo", "GDS": "Sistema global de reservas (GDS)",
    },
    # En el orden de frecuencia de los datos limpios: 82 %, 13 %, 4 % y menos del 1 %
    "tipo_cliente": {
        "Transient": "Transitorio (individual)", "Transient-Party": "Transitorio asociado",
        "Contract": "Contrato", "Group": "Grupo",
    },
    "tipo_deposito": {
        "No Deposit": "Sin depósito", "Non Refund": "No reembolsable", "Refundable": "Reembolsable",
    },
    "pais_origen": NOMBRES_PAISES,
    # Las letras son anónimas en el dataset; se orienta con la proporción de reservas de los datos limpios
    "habitacion_reservada": {
        "A": "A (la más común: 65 % de las reservas)",
        "B": "B (1 % de las reservas)",
        "C": "C (1 % de las reservas)",
        "D": "D (20 % de las reservas)",
        "E": "E (7 % de las reservas)",
        "F": "F (3 % de las reservas)",
        "G": "G (2 % de las reservas)",
        "H": "H (menos del 1 % de las reservas)",
        "L": "L (menos del 1 % de las reservas)",
    },
}

# Niveles de riesgo: alto desde el umbral; medio entre el promedio del hotel y el umbral
# El umbral se elige en porcentaje; el mínimo queda por encima del promedio del hotel para que exista el riesgo medio
UMBRAL_MINIMO = 30
UMBRAL_MAXIMO = 80
PASO_UMBRAL = 5
RECOMENDACIONES = {
    "alto": "Confirmar la reserva con el cliente o pedir un depósito.",
    "medio": "Hacer seguimiento a la reserva antes de la llegada.",
    "bajo": "No requiere acciones adicionales.",
}
COLORES_RIESGO = {"alto": "red", "medio": "orange", "bajo": "green"}

# Pantalla de inicio
DESCRIPCION_APLICACION = (
    "Aplicación que estima la probabilidad de que una reserva hotelera sea cancelada, usando un modelo "
    "Gradient Boosting entrenado con 86.637 reservas reales de dos hoteles."
)
FUNCIONES_APLICACION = [
    {
        "icono": "reserva",
        "titulo": "Predicción",
        "texto": "Ingresa los datos de una reserva y obtén su riesgo de cancelación al instante.",
    },
    {
        "icono": "ajustes",
        "titulo": "Ejemplos y umbral",
        "texto": "Carga reservas de ejemplo y define desde qué probabilidad el riesgo es alto.",
    },
    {
        "icono": "libro",
        "titulo": "Cómo funciona",
        "texto": "Conoce qué datos usa el modelo, cómo leer el resultado y sus limitaciones.",
    },
]
CREDITOS = {
    "universidad": "Universidad Santo Tomás",
    "programa": "Maestría en Análisis de Datos y Sistemas Inteligentes",
    "estudiantes": ["Omar Alberto Torres", "Diego Alejandro Roa Lara", "Jorge Enrique Alvarez Martinez"],
    "docente": "Gerardo Humberto Valencia Rivera",
    "fecha": "Noviembre de 2026",
}
