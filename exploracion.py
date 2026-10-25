"""Extracción y análisis exploratorio: descarga, lectura, renombrado, nulos, distribuciones, correlación y asociación."""
import math
import os

import kagglehub
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from constantes import (
    ASIMETRIA_COLA_LARGA, COLOR_BARRAS, LIMITES_VALOR_INFORMACION, LIMITES_V_CRAMER, METODOS_CORRELACION,
    NIVELES_ASOCIACION, NIVELES_PODER_PREDICTIVO, NOMBRES_EN_ESPANOL, NOMBRE_ARCHIVO_DATOS,
    NOMBRE_DATASET_KAGGLE, UMBRAL_CATEGORIAS, UMBRAL_CORRELACION_DEBIL, UMBRAL_DIFERENCIA,
    UMBRAL_INFORMACION_SOSPECHOSA, UMBRAL_SIN_ASOCIACION, UMBRAL_SIN_CORRELACION, VARIABLE_OBJETIVO,
)


# Paso 2. Descarga y lectura del dataset
def descargar_datos() -> str:
    """Descarga la última versión del dataset desde Kaggle y devuelve la carpeta donde quedó guardado."""
    carpeta = kagglehub.dataset_download(NOMBRE_DATASET_KAGGLE)
    print("Carpeta del dataset:", carpeta)
    return carpeta


def leer_datos(carpeta: str) -> pd.DataFrame:
    """Lee el archivo de reservas de la carpeta indicada y lo devuelve como tabla de pandas."""
    ruta_archivo = os.path.join(carpeta, NOMBRE_ARCHIVO_DATOS)
    return pd.read_csv(ruta_archivo)


# Paso 3. Renombrado de variables al español
def renombrar_columnas(datos: pd.DataFrame) -> pd.DataFrame:
    """Traduce al español los nombres de las columnas; se detiene si alguna no tiene traducción."""
    for columna in datos.columns:
        if columna not in NOMBRES_EN_ESPANOL:
            raise ValueError(f"La columna {columna} no tiene traducción al español.")
    return datos.rename(columns=NOMBRES_EN_ESPANOL)


# Paso 7. Análisis de valores nulos y filas duplicadas
def tabular_nulos(datos: pd.DataFrame) -> pd.DataFrame:
    """Cuenta los valores nulos de cada variable y su porcentaje; solo muestra las que tienen nulos."""
    tabla = pd.DataFrame({
        "nulos": datos.isna().sum(),
        "porcentaje_nulos": (datos.isna().mean() * 100).round(2),
    })
    tabla = tabla[tabla["nulos"] > 0]
    return tabla.sort_values("porcentaje_nulos", ascending=False)


def tabular_duplicados(datos: pd.DataFrame) -> pd.DataFrame:
    """Cuenta las filas duplicadas del dataset y su porcentaje."""
    filas_duplicadas = datos.duplicated().sum()
    return pd.DataFrame({
        "filas_totales": [len(datos)],
        "filas_duplicadas": [filas_duplicadas],
        "porcentaje_duplicados": [round(filas_duplicadas / len(datos) * 100, 2)],
    })


# Paso 9. Distribución de las variables numéricas
def graficar_histogramas(datos: pd.DataFrame, variables: list[str]) -> None:
    """Dibuja un histograma por variable, con su asimetría en el título, en una cuadrícula de 4 columnas."""
    cantidad_filas = math.ceil(len(variables) / 4)
    plt.figure(figsize=(18, 4 * cantidad_filas))
    posicion = 1
    for variable in variables:
        plt.subplot(cantidad_filas, 4, posicion)
        plt.hist(datos[variable].dropna(), bins=50, color=COLOR_BARRAS, edgecolor="white", linewidth=0.4)
        plt.title(f"{variable}\nasimetría = {datos[variable].skew():.2f}")
        plt.ylabel("frecuencia")
        posicion = posicion + 1
    plt.tight_layout()
    plt.show()


# Paso 10. Tabla de asimetría y colas de las variables numéricas
def tabular_asimetria(datos: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    """Resume la asimetría, el porcentaje de ceros y los valores extremos de cada variable numérica."""
    tabla = pd.DataFrame({
        "asimetria": datos[variables].skew(),
        "porcentaje_ceros": (datos[variables] == 0).mean() * 100,
        "mediana": datos[variables].median(),
        "percentil_99": datos[variables].quantile(0.99),
        "maximo": datos[variables].max(),
    })
    tabla = tabla.round(2)
    tabla = tabla.sort_values("asimetria", ascending=False)

    # Cola larga: asimetría mayor que 1 hacia cualquiera de los dos lados
    tabla["cola_larga"] = tabla["asimetria"].abs() > ASIMETRIA_COLA_LARGA
    return tabla


# Paso 11. Comparación de transformaciones para las variables con cola larga
def graficar_transformaciones(datos: pd.DataFrame, variables: list[str]) -> None:
    """Grafica cada variable original, con logaritmo y con raíz cuadrada, para quedarnos con la de menor asimetría."""
    for variable in variables:
        serie = datos[variable].clip(lower=0)   # evita valores negativos

        original = serie
        logaritmo = np.log1p(serie)             # log(x + 1), funciona con ceros
        raiz = np.sqrt(serie)

        plt.figure(figsize=(16, 4))

        plt.subplot(1, 3, 1)                    # 1 fila, 3 columnas, gráfico 1
        plt.hist(original, bins=50, color=COLOR_BARRAS)
        plt.title(f"{variable} original\nasimetría = {original.skew():.2f}")

        plt.subplot(1, 3, 2)                    # gráfico 2
        plt.hist(logaritmo, bins=50, color=COLOR_BARRAS)
        plt.title(f"{variable} logaritmo\nasimetría = {logaritmo.skew():.2f}")

        plt.subplot(1, 3, 3)                    # gráfico 3
        plt.hist(raiz, bins=50, color=COLOR_BARRAS)
        plt.title(f"{variable} raíz cuadrada\nasimetría = {raiz.skew():.2f}")

        plt.tight_layout()
        plt.show()


# Paso 12. Distribución de las variables categóricas nominales
def preparar_categoria(serie: pd.Series) -> pd.Series:
    """Convierte la variable a texto y pone Sin dato donde hay vacíos."""
    serie = serie.fillna("Sin dato")
    serie = serie.astype(str)
    serie = serie.str.removesuffix(".0")   # el código 9.0 pasa a ser 9
    return serie


def graficar_nominales(datos: pd.DataFrame, variables: list[str], maximo_categorias: int) -> None:
    """Dibuja el porcentaje de reservas de cada categoría; agrupa en Otras las que superan el máximo."""
    for variable in variables:
        categorias = preparar_categoria(datos[variable])

        # Porcentaje de reservas por categoría (de mayor a menor)
        porcentajes = categorias.value_counts(normalize=True) * 100

        # Si hay muchas categorías, se dejan las principales y el resto va a "Otras"
        if len(porcentajes) > maximo_categorias:
            resto = porcentajes.iloc[maximo_categorias:].sum()
            porcentajes = porcentajes.iloc[:maximo_categorias].copy()
            porcentajes["Otras"] = resto

        # Orden de menor a mayor para que la barra más grande quede arriba
        porcentajes = porcentajes.sort_values()

        plt.figure(figsize=(10, 5))
        barras = plt.barh(porcentajes.index, porcentajes.values, color=COLOR_BARRAS)
        plt.bar_label(barras, fmt="%.1f%%", fontsize=8, padding=2)
        plt.title(f"{variable} ({datos[variable].nunique()} categorías)")
        plt.xlabel("porcentaje de reservas (%)")
        plt.tight_layout()
        plt.show()


# Paso 13. Distribución de las variables categóricas ordinales
def graficar_ordinales(datos: pd.DataFrame, orden: dict[str, list[str]]) -> None:
    """Dibuja el porcentaje de reservas de cada categoría, respetando su orden natural."""
    for variable in orden:
        categorias = orden[variable]   # orden correcto, por ejemplo: enero, febrero, marzo

        # Porcentaje de reservas por categoría
        porcentajes = datos[variable].value_counts(normalize=True) * 100

        # Acomoda las categorías en su orden natural (no de mayor a menor)
        porcentajes = porcentajes.reindex(categorias)

        plt.figure(figsize=(10, 5))
        barras = plt.bar(porcentajes.index, porcentajes.values, color=COLOR_BARRAS)
        plt.bar_label(barras, fmt="%.1f%%", fontsize=8, padding=2)
        plt.title(variable)
        plt.ylabel("porcentaje de reservas (%)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# Paso 14. Correlación de Pearson, Spearman y Kendall de las variables numéricas con la variable objetivo
def advertir_correlacion(fila: pd.Series) -> str:
    """Devuelve la alerta de una variable según sus tres correlaciones con la variable objetivo."""
    maxima = fila[METODOS_CORRELACION].abs().max()
    if maxima < UMBRAL_SIN_CORRELACION:
        return "ALERTA: sin correlación"
    if abs(fila["pearson"] - fila["spearman"]) > UMBRAL_DIFERENCIA:
        return "ALERTA: relación no lineal o afectada por atípicos"
    if maxima < UMBRAL_CORRELACION_DEBIL:
        return "ALERTA: correlación muy débil"
    return "Sin alerta"


def tabular_correlaciones(datos: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    """Calcula Pearson, Spearman y Kendall de cada variable con la variable objetivo y agrega su alerta."""
    tabla = pd.DataFrame()

    # Construimos una columna por cada método de correlación
    for metodo in METODOS_CORRELACION:
        tabla[metodo] = datos[variables].corrwith(datos[VARIABLE_OBJETIVO], method=metodo)
    tabla = tabla.round(3)

    # Revisa cada variable y escribe una advertencia si hace falta
    advertencias = []
    for variable in tabla.index:
        advertencias.append(advertir_correlacion(tabla.loc[variable]))
    tabla["advertencia"] = advertencias

    # Ordena de la relación más fuerte a la más débil según Spearman
    orden = tabla["spearman"].abs().sort_values(ascending=False).index
    return tabla.loc[orden]


# Paso 15. Asociación de las variables categóricas nominales con la variable objetivo
def v_de_cramer(categoria: pd.Series, objetivo: pd.Series) -> float:
    """Mide de 0 a 1 la fuerza de asociación entre dos variables categóricas, con corrección de sesgo."""
    tabla = pd.crosstab(categoria, objetivo).to_numpy()
    total = tabla.sum()

    # Reservas que se esperarían en cada casilla si no hubiera relación entre las variables
    totales_por_fila = tabla.sum(axis=1, keepdims=True)
    totales_por_columna = tabla.sum(axis=0, keepdims=True)
    esperados = totales_por_fila * totales_por_columna / total
    chi_cuadrado = ((tabla - esperados) ** 2 / esperados).sum()

    # Corrección de sesgo para tablas grandes
    cantidad_filas = tabla.shape[0]
    cantidad_columnas = tabla.shape[1]
    phi_corregido = max(0, chi_cuadrado / total - (cantidad_columnas - 1) * (cantidad_filas - 1) / (total - 1))
    filas_corregidas = cantidad_filas - (cantidad_filas - 1) ** 2 / (total - 1)
    columnas_corregidas = cantidad_columnas - (cantidad_columnas - 1) ** 2 / (total - 1)
    return np.sqrt(phi_corregido / min(columnas_corregidas - 1, filas_corregidas - 1))


def valor_informacion(categoria: pd.Series, objetivo: pd.Series) -> float:
    """Mide el poder de una variable categórica para separar reservas canceladas de no canceladas."""
    tabla = pd.crosstab(categoria, objetivo) + 0.5  # suavizado para categorías sin canceladas o sin no canceladas
    reparto_canceladas = tabla[1] / tabla[1].sum()
    reparto_no_canceladas = tabla[0] / tabla[0].sum()
    peso_evidencia = np.log(reparto_canceladas / reparto_no_canceladas)
    return ((reparto_canceladas - reparto_no_canceladas) * peso_evidencia).sum()


def advertir_asociacion(fila: pd.Series) -> str:
    """Devuelve la alerta de una variable según su V de Cramér, su valor de información y su número de categorías."""
    avisos = []
    if fila["v_cramer"] < UMBRAL_SIN_ASOCIACION:
        avisos.append("sin asociación")
    if fila["valor_informacion"] > UMBRAL_INFORMACION_SOSPECHOSA:
        avisos.append("valor de información sospechoso, revisar fuga de datos")
    if fila["categorias"] > UMBRAL_CATEGORIAS:
        avisos.append("muchas categorías, valores inflados")

    if len(avisos) == 0:
        return "Sin alerta"
    return "ALERTA: " + "; ".join(avisos)


def tabular_asociacion(datos: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    """Calcula la V de Cramér y el valor de información de cada variable con la variable objetivo, con su interpretación y alerta."""
    objetivo = datos[VARIABLE_OBJETIVO]
    filas = []
    for variable in variables:
        categoria = preparar_categoria(datos[variable])
        filas.append({
            "variable": variable,
            "categorias": categoria.nunique(),
            "v_cramer": v_de_cramer(categoria, objetivo),
            "valor_informacion": valor_informacion(categoria, objetivo),
        })
    tabla = pd.DataFrame(filas)
    tabla = tabla.set_index("variable")
    tabla = tabla.round(3)

    # Interpretación de cada medida según sus rangos
    tabla["asociacion"] = pd.cut(tabla["v_cramer"], bins=LIMITES_V_CRAMER, labels=NIVELES_ASOCIACION, right=False)
    tabla["poder_predictivo"] = pd.cut(
        tabla["valor_informacion"], bins=LIMITES_VALOR_INFORMACION, labels=NIVELES_PODER_PREDICTIVO, right=False,
    )

    advertencias = []
    for variable in tabla.index:
        advertencias.append(advertir_asociacion(tabla.loc[variable]))
    tabla["advertencia"] = advertencias
    return tabla.sort_values("valor_informacion", ascending=False)
