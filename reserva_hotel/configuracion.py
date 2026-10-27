"""Constantes de la aplicación: rutas, transformaciones, rangos de los campos, etiquetas y colores."""
import os

from reserva_hotel.paises import NOMBRES_PAISES

# Rutas
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_MODELO = os.path.join(CARPETA_PROYECTO, "modelos", "modelo_cancelaciones.joblib")

# Tasa de cancelación de los datos limpios del notebook (Paso 25): separa el riesgo bajo del medio
TASA_CANCELACION_DATOS = 0.277

# Nombre en español de cada tipo de modelo
NOMBRES_MODELOS = {
    "LogisticRegression": "Regresión logística",
    "RandomForestClassifier": "Random Forest",
    "HistGradientBoostingClassifier": "Gradient Boosting",
}

# Transformaciones: deben ser las mismas del notebook
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

# Variables del modelo que dependen de cada campo de entrada.
# Un campo solo se muestra si el modelo usa la variable que se calcula con él.
VARIABLE_DE_CADA_CAMPO = {
    "fecha_llegada": "mes_llegada",
    "dias_anticipacion": "dias_anticipacion",
    "noches_fin_semana": "noches_fin_semana",
    "noches_entre_semana": "noches_entre_semana",
    "adultos": "adultos",
    "ninos": "tiene_hijos",
    "bebes": "tiene_hijos",
    "regimen_comidas": "regimen_comidas",
    "tipo_hotel": "tipo_hotel",
    "pais_origen": "pais_origen",
    "segmento_mercado": "segmento_mercado",
    "canal_distribucion": "canal_distribucion",
    "agente": "agente",
    "tipo_cliente": "tipo_cliente",
    "tipo_deposito": "tipo_deposito",
    "habitacion_reservada": "habitacion_reservada",
    "cliente_recurrente": "cliente_recurrente",
    "cancelaciones_previas": "tuvo_cancelaciones_previas",
    "reservas_previas_no_canceladas": "tuvo_reservas_previas",
    "cambios_reserva": "cambios_reserva",
    "dias_lista_espera": "estuvo_en_lista_espera",
    "tarifa_diaria_promedio": "tarifa_diaria_promedio",
    "solicitudes_especiales": "solicitudes_especiales",
    "parqueaderos_solicitados": "solicito_parqueadero",
    "empresa": "tiene_empresa",
}

# Rangos de los campos numéricos
DIAS_ANTICIPACION_MAXIMOS = 737
NOCHES_FIN_SEMANA_MAXIMAS = 19
NOCHES_ENTRE_SEMANA_MAXIMAS = 50
# Se permiten más adultos que MAXIMO_ADULTOS; el modelo trata igual las reservas de 4 o más
ADULTOS_MAXIMOS = 10
NINOS_MAXIMOS = 10
BEBES_MAXIMOS = 10
HISTORIAL_MAXIMO = 72
CAMBIOS_MAXIMOS = 21
DIAS_LISTA_ESPERA_MAXIMOS = 391
TARIFA_MAXIMA = 1000
SOLICITUDES_MAXIMAS = 5

# Ejemplos para probar la aplicación sin llenar todos los campos
EJEMPLOS = {
    "Riesgo bajo": {
        "fecha_llegada": "2026-03-14", "dias_anticipacion": 30, "noches_fin_semana": 1,
        "noches_entre_semana": 2, "adultos": 2, "ninos": 0, "bebes": 0, "regimen_comidas": "BB",
        "tipo_hotel": "Resort Hotel", "pais_origen": "GBR", "segmento_mercado": "Direct",
        "canal_distribucion": "Direct", "agente": "Sin agente", "tipo_cliente": "Transient",
        "tipo_deposito": "No Deposit", "habitacion_reservada": "A", "cliente_recurrente": 0,
        "cancelaciones_previas": 0, "reservas_previas_no_canceladas": 0, "cambios_reserva": 1,
        "dias_lista_espera": 0, "tarifa_diaria_promedio": 90, "solicitudes_especiales": 1,
        "parqueaderos_solicitados": 0, "empresa": False,
    },
    "Riesgo medio": {
        "fecha_llegada": "2026-07-10", "dias_anticipacion": 60, "noches_fin_semana": 2,
        "noches_entre_semana": 3, "adultos": 2, "ninos": 0, "bebes": 0, "regimen_comidas": "BB",
        "tipo_hotel": "City Hotel", "pais_origen": "FRA", "segmento_mercado": "Online TA",
        "canal_distribucion": "TA/TO", "agente": "9", "tipo_cliente": "Transient",
        "tipo_deposito": "No Deposit", "habitacion_reservada": "A", "cliente_recurrente": 0,
        "cancelaciones_previas": 0, "reservas_previas_no_canceladas": 0, "cambios_reserva": 0,
        "dias_lista_espera": 0, "tarifa_diaria_promedio": 120, "solicitudes_especiales": 1,
        "parqueaderos_solicitados": 0, "empresa": False,
    },
    "Riesgo alto": {
        "fecha_llegada": "2026-08-15", "dias_anticipacion": 250, "noches_fin_semana": 2,
        "noches_entre_semana": 5, "adultos": 2, "ninos": 0, "bebes": 0, "regimen_comidas": "BB",
        "tipo_hotel": "City Hotel", "pais_origen": "PRT", "segmento_mercado": "Groups",
        "canal_distribucion": "TA/TO", "agente": "1", "tipo_cliente": "Transient",
        "tipo_deposito": "No Deposit", "habitacion_reservada": "A", "cliente_recurrente": 0,
        "cancelaciones_previas": 0, "reservas_previas_no_canceladas": 0, "cambios_reserva": 0,
        "dias_lista_espera": 0, "tarifa_diaria_promedio": 100, "solicitudes_especiales": 0,
        "parqueaderos_solicitados": 0, "empresa": False,
    },
}
EJEMPLO_INICIAL = "Riesgo medio"

# Etiquetas en español de las categorías que se muestran en las listas
ETIQUETAS_CATEGORIAS = {
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
        "TA/TO": "Agencia u operador", "Direct": "Directo",
        "Corporate": "Corporativo", "GDS": "Sistema global de reservas",
    },
    "tipo_cliente": {
        "Transient": "Individual", "Transient-Party": "Individual ligado a otra reserva",
        "Contract": "Por contrato", "Group": "Grupo",
    },
    "tipo_deposito": {
        "No Deposit": "Sin depósito", "Non Refund": "No reembolsable", "Refundable": "Reembolsable",
    },
    "agente": {"Sin agente": "Sin agente"},
    "pais_origen": NOMBRES_PAISES,
    # Las letras son anónimas en el dataset; se orienta con la proporción de reservas y la tarifa
    # mediana por noche de cada tipo en los datos limpios del notebook
    "habitacion_reservada": {
        "A": "A (la más común: 65 % de las reservas, tarifa típica 89 €)",
        "B": "B (1 % de las reservas, tarifa típica 87 €)",
        "C": "C (1 % de las reservas, tarifa típica 164 €)",
        "D": "D (20 % de las reservas, tarifa típica 123 €)",
        "E": "E (7 % de las reservas, tarifa típica 116 €)",
        "F": "F (3 % de las reservas, tarifa típica 177 €)",
        "G": "G (2 % de las reservas, tarifa típica 178 €)",
        "H": "H (1 % de las reservas, tarifa típica 185 €, grupos más grandes)",
        "L": "L (muy poco común, tarifa típica 143 €)",
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
