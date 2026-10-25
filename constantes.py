"""Constantes del proyecto: datos, grupos de variables, umbrales, parámetros de los modelos, rutas y colores."""
import os

import joblib
import numpy as np
import pandas as pd
import sklearn

# Datos
NOMBRE_DATASET_KAGGLE = "jessemostipak/hotel-booking-demand"
NOMBRE_ARCHIVO_DATOS = "hotel_bookings.csv"

# Traducción de cada nombre original (inglés) a su nombre en español,
# para tener un contexto más natural
NOMBRES_EN_ESPANOL = {
    "hotel": "tipo_hotel",
    "is_canceled": "target_cancelada",
    "lead_time": "dias_anticipacion",
    "arrival_date_year": "anio_llegada",
    "arrival_date_month": "mes_llegada",
    "arrival_date_week_number": "semana_llegada",
    "arrival_date_day_of_month": "dia_llegada",
    "stays_in_weekend_nights": "noches_fin_semana",
    "stays_in_week_nights": "noches_entre_semana",
    "adults": "adultos",
    "children": "ninos",
    "babies": "bebes",
    "meal": "regimen_comidas",
    "country": "pais_origen",
    "market_segment": "segmento_mercado",
    "distribution_channel": "canal_distribucion",
    "is_repeated_guest": "cliente_recurrente",
    "previous_cancellations": "cancelaciones_previas",
    "previous_bookings_not_canceled": "reservas_previas_no_canceladas",
    "reserved_room_type": "habitacion_reservada",
    "assigned_room_type": "habitacion_asignada",
    "booking_changes": "cambios_reserva",
    "deposit_type": "tipo_deposito",
    "agent": "agente",
    "company": "empresa",
    "days_in_waiting_list": "dias_lista_espera",
    "customer_type": "tipo_cliente",
    "adr": "tarifa_diaria_promedio",
    "required_car_parking_spaces": "parqueaderos_solicitados",
    "total_of_special_requests": "solicitudes_especiales",
    "reservation_status": "estado_reserva",
    "reservation_status_date": "fecha_estado_reserva",
}

VARIABLE_OBJETIVO = "target_cancelada"

# Grupos de variables
VARIABLES_NUMERICAS = [
    "dias_anticipacion", "anio_llegada", "semana_llegada", "dia_llegada",
    "noches_fin_semana", "noches_entre_semana", "adultos", "ninos", "bebes",
    "cliente_recurrente", "cancelaciones_previas", "reservas_previas_no_canceladas",
    "cambios_reserva", "dias_lista_espera", "tarifa_diaria_promedio",
    "parqueaderos_solicitados", "solicitudes_especiales",
]
VARIABLES_NOMINALES = [
    "tipo_hotel", "pais_origen", "segmento_mercado", "canal_distribucion",
    "habitacion_reservada", "habitacion_asignada", "tipo_deposito",
    "agente", "empresa", "tipo_cliente",
]
VARIABLES_ORDINALES = ["mes_llegada", "regimen_comidas"]

# Orden natural de las categorías de cada variable ordinal
ORDEN_ORDINALES = {
    "mes_llegada": ["January", "February", "March", "April", "May", "June", "July",
                    "August", "September", "October", "November", "December"],
    "regimen_comidas": ["Undefined", "SC", "BB", "HB", "FB"],
}

# Variables continuas con cola larga, candidatas a transformarse
VARIABLES_A_TRANSFORMAR = ["dias_anticipacion", "noches_fin_semana", "noches_entre_semana", "tarifa_diaria_promedio"]

# Análisis exploratorio
MAXIMO_CATEGORIAS_GRAFICO = 10
ASIMETRIA_COLA_LARGA = 1

METODOS_CORRELACION = ["pearson", "spearman", "kendall"]
UMBRAL_SIN_CORRELACION = 0.05
UMBRAL_CORRELACION_DEBIL = 0.10
UMBRAL_DIFERENCIA = 0.10

UMBRAL_SIN_ASOCIACION = 0.10
UMBRAL_INFORMACION_SOSPECHOSA = 0.50
UMBRAL_CATEGORIAS = 20
LIMITES_V_CRAMER = [-np.inf, 0.10, 0.30, 0.50, np.inf]
NIVELES_ASOCIACION = ["despreciable", "débil", "moderada", "fuerte"]
LIMITES_VALOR_INFORMACION = [-np.inf, 0.02, 0.10, 0.30, 0.50, np.inf]
NIVELES_PODER_PREDICTIVO = ["no predictiva", "débil", "media", "fuerte", "sospechoso"]

# Limpieza y transformación
# Columnas que se eliminan y el motivo de cada una
COLUMNAS_A_ELIMINAR = {
    "estado_reserva": "revela si la reserva se canceló",
    "fecha_estado_reserva": "revela cuándo se canceló o se cumplió la reserva",
    "habitacion_asignada": "se asigna al llegar, algo que no ocurre si se cancela",
    "anio_llegada": "no sirve para predecir años futuros",
}
TARIFA_MAXIMA_VALIDA = 1000

# Categoría más frecuente de cada variable, según el Paso 12
CATEGORIA_MAS_FRECUENTE = {
    "canal_distribucion": "TA/TO",
    "segmento_mercado": "Online TA",
}

# Variable original y nombre del indicador que la reemplaza
INDICADORES_BINARIOS = {
    "cancelaciones_previas": "tuvo_cancelaciones_previas",
    "reservas_previas_no_canceladas": "tuvo_reservas_previas",
    "dias_lista_espera": "estuvo_en_lista_espera",
    "parqueaderos_solicitados": "solicito_parqueadero",
}

VARIABLES_CON_LOGARITMO = ["noches_entre_semana", "noches_fin_semana"]
MAXIMO_ADULTOS = 4

# Número de cada mes, de 1 (enero) a 12 (diciembre)
CODIGOS_MES = {}
numero_mes = 1
for mes in ORDEN_ORDINALES["mes_llegada"]:
    CODIGOS_MES[mes] = numero_mes
    numero_mes = numero_mes + 1

CODIGOS_REGIMEN = {"SC": 0, "BB": 1, "HB": 2, "FB": 3}

# Rango esperado de la tasa de cancelación del dataset limpio
TASA_CANCELACION_MINIMA = 0.20
TASA_CANCELACION_MAXIMA = 0.40

RUTA_DATOS_LIMPIOS = "reservas_limpias.csv"

# Modelado
PROPORCION_PRUEBA = 0.20
SEMILLA = 42

PREDICTORAS_CATEGORICAS = [
    "tipo_hotel", "pais_origen", "segmento_mercado", "canal_distribucion",
    "habitacion_reservada", "tipo_deposito", "agente", "tipo_cliente",
]
FRECUENCIA_MINIMA_CATEGORIA = 0.01

MAXIMO_ITERACIONES_LOGISTICA = 1000
ARBOLES_RANDOM_FOREST = 300
MINIMO_RESERVAS_POR_HOJA = 5

REPETICIONES_PERMUTACION = 5
APORTE_MINIMO = 0.001
UMBRAL_SOBREAJUSTE = 0.05

# Experimentos
COLUMNAS_EXCLUIDAS_EXPERIMENTO_1 = ["semana_llegada"]
COLUMNAS_EXCLUIDAS_EXPERIMENTO_2 = ["mes_llegada"]

# Exportación
CARPETA_MODELOS = "modelos"
RUTA_MODELO = os.path.join(CARPETA_MODELOS, "modelo_cancelaciones.joblib")
UMBRAL_DECISION = 0.5
LIBRERIAS_APLICACION = {"scikit-learn": sklearn, "pandas": pd, "numpy": np, "joblib": joblib}

# Gráficos
COLOR_BARRAS = "#2a78d6"
COLOR_BAJO_APORTE = "#bdbdbd"
COLORES_MODELOS = ["#2a78d6", "#eb6834", "#1baf7a"]
