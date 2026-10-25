"""Modelado: división de los datos, pipelines, entrenamiento, métricas, matrices de confusión, curvas ROC e importancia."""
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from matplotlib.patches import Patch
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    RocCurveDisplay, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from constantes import (
    APORTE_MINIMO, ARBOLES_RANDOM_FOREST, COLORES_MODELOS, COLOR_BAJO_APORTE, COLOR_BARRAS,
    FRECUENCIA_MINIMA_CATEGORIA, MAXIMO_ITERACIONES_LOGISTICA, MINIMO_RESERVAS_POR_HOJA,
    PREDICTORAS_CATEGORICAS, PROPORCION_PRUEBA, REPETICIONES_PERMUTACION, SEMILLA, VARIABLE_OBJETIVO,
)


# Paso 27. División estratificada en entrenamiento y prueba
def dividir_datos(datos: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Separa predictoras y objetivo, y las divide en entrenamiento y prueba manteniendo la proporción de canceladas."""
    predictoras = datos.drop(columns=VARIABLE_OBJETIVO)
    objetivo = datos[VARIABLE_OBJETIVO]
    return train_test_split(
        predictoras, objetivo,
        test_size=PROPORCION_PRUEBA, stratify=objetivo, random_state=SEMILLA,
    )


def comparar_division(objetivo: pd.Series, objetivo_entrenamiento: pd.Series, objetivo_prueba: pd.Series) -> pd.DataFrame:
    """Compara el número de reservas y la tasa de cancelación del total, del entrenamiento y de la prueba."""
    return pd.DataFrame(
        {
            "reservas": [len(objetivo), len(objetivo_entrenamiento), len(objetivo_prueba)],
            "porcentaje_canceladas": [
                round(objetivo.mean() * 100, 2),
                round(objetivo_entrenamiento.mean() * 100, 2),
                round(objetivo_prueba.mean() * 100, 2),
            ],
        },
        index=["total", "entrenamiento", "prueba"],
    )


# Paso 28. Preparación, creación y entrenamiento de los modelos (se usan en los tres experimentos)
def elegir_predictoras(columnas: list[str], columnas_excluidas: list[str]) -> list[str]:
    """Devuelve las predictoras de un experimento: todas las columnas disponibles menos las excluidas."""
    predictoras = []
    for columna in columnas:
        if columna not in columnas_excluidas:
            predictoras.append(columna)
    return predictoras


def crear_preparacion(escalar: bool, predictoras: list[str]) -> ColumnTransformer:
    """Convierte las categóricas en columnas de 0 y 1, agrupando las poco frecuentes, y escala las numéricas solo si se indica."""
    categoricas = []
    numericas = []
    for columna in predictoras:
        if columna in PREDICTORAS_CATEGORICAS:
            categoricas.append(columna)
        else:
            numericas.append(columna)

    codificador = OneHotEncoder(
        min_frequency=FRECUENCIA_MINIMA_CATEGORIA,
        handle_unknown="infrequent_if_exist",
        sparse_output=False,
    )

    # Solo la regresión logística necesita escalar; los árboles reciben las numéricas sin cambios
    if escalar:
        tratamiento_numericas = StandardScaler()
    else:
        tratamiento_numericas = "passthrough"

    return ColumnTransformer([
        ("categoricas", codificador, categoricas),
        ("numericas", tratamiento_numericas, numericas),
    ])


def crear_modelos(predictoras: list[str]) -> dict[str, Pipeline]:
    """Crea los pipelines de regresión logística (con escalado), Random Forest y Gradient Boosting (sin escalado)."""
    regresion_logistica = Pipeline([
        ("preparacion", crear_preparacion(escalar=True, predictoras=predictoras)),
        ("modelo", LogisticRegression(class_weight="balanced", max_iter=MAXIMO_ITERACIONES_LOGISTICA)),
    ])
    random_forest = Pipeline([
        ("preparacion", crear_preparacion(escalar=False, predictoras=predictoras)),
        ("modelo", RandomForestClassifier(
            n_estimators=ARBOLES_RANDOM_FOREST, min_samples_leaf=MINIMO_RESERVAS_POR_HOJA,
            class_weight="balanced", n_jobs=-1, random_state=SEMILLA,
        )),
    ])
    gradient_boosting = Pipeline([
        ("preparacion", crear_preparacion(escalar=False, predictoras=predictoras)),
        ("modelo", HistGradientBoostingClassifier(class_weight="balanced", random_state=SEMILLA)),
    ])
    return {
        "Regresión logística": regresion_logistica,
        "Random Forest": random_forest,
        "Gradient Boosting": gradient_boosting,
    }


def entrenar_modelos(modelos: dict[str, Pipeline], predictoras: pd.DataFrame, objetivo: pd.Series) -> dict[str, Pipeline]:
    """Entrena cada pipeline con los datos de entrenamiento."""
    for nombre in modelos:
        modelos[nombre].fit(predictoras, objetivo)
        print("Entrenado:", nombre)
    return modelos


# Paso 29. Métricas de cada modelo en entrenamiento y prueba
def calcular_metricas(modelo: Pipeline, predictoras: pd.DataFrame, objetivo: pd.Series) -> dict[str, float]:
    """Calcula precisión, recall, F1 y AUC de un modelo sobre un conjunto de datos."""
    prediccion = modelo.predict(predictoras)
    probabilidad_cancelar = modelo.predict_proba(predictoras)[:, 1]   # columna de la clase "cancelada"
    return {
        "precision": precision_score(objetivo, prediccion),
        "recall": recall_score(objetivo, prediccion),
        "f1": f1_score(objetivo, prediccion),
        "auc": roc_auc_score(objetivo, probabilidad_cancelar),
    }


def tabular_metricas_modelo(modelo: Pipeline, conjuntos: dict[str, tuple[pd.DataFrame, pd.Series]]) -> pd.DataFrame:
    """Muestra cada métrica de un modelo en entrenamiento y en prueba, y la diferencia entre ambas."""
    tabla = pd.DataFrame()
    for nombre_conjunto in conjuntos:
        predictoras, objetivo = conjuntos[nombre_conjunto]
        tabla[nombre_conjunto] = pd.Series(calcular_metricas(modelo, predictoras, objetivo))
    tabla["diferencia"] = tabla["entrenamiento"] - tabla["prueba"]
    return tabla.round(3)


def evaluar_modelos(
    modelos: dict[str, Pipeline], conjuntos: dict[str, tuple[pd.DataFrame, pd.Series]], mostrar: bool,
) -> dict[str, pd.DataFrame]:
    """Calcula la tabla de entrenamiento y prueba de cada modelo y la muestra si se indica."""
    metricas_por_modelo = {}
    for nombre in modelos:
        metricas_por_modelo[nombre] = tabular_metricas_modelo(modelos[nombre], conjuntos)
        if mostrar:
            print(nombre)
            display(metricas_por_modelo[nombre])
    return metricas_por_modelo


# Paso 30. Comparación de los modelos
def comparar_modelos(metricas_por_modelo: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Reúne las métricas de prueba de cada modelo en una sola tabla, ordenada por F1 y AUC."""
    filas = []
    for nombre in metricas_por_modelo:
        tabla = metricas_por_modelo[nombre]
        filas.append({
            "modelo": nombre,
            "precision": tabla.loc["precision", "prueba"],
            "recall": tabla.loc["recall", "prueba"],
            "f1": tabla.loc["f1", "prueba"],
            "auc": tabla.loc["auc", "prueba"],
        })
    comparacion = pd.DataFrame(filas)
    comparacion = comparacion.set_index("modelo")
    return comparacion.sort_values(["f1", "auc"], ascending=False)


# Paso 31. Matrices de confusión en prueba
def tabular_matrices_confusion(modelos: dict[str, Pipeline], predictoras: pd.DataFrame, objetivo: pd.Series) -> pd.DataFrame:
    """Muestra, para cada modelo, los cuatro valores de su matriz de confusión en prueba con su precisión, recall y F1."""
    filas = []
    for nombre in modelos:
        prediccion = modelos[nombre].predict(predictoras)
        matriz = confusion_matrix(objetivo, prediccion)   # filas: realidad; columnas: predicción
        filas.append({
            "modelo": nombre,
            "no_canceladas_acertadas": matriz[0, 0],
            "falsas_alarmas": matriz[0, 1],
            "cancelaciones_no_detectadas": matriz[1, 0],
            "cancelaciones_detectadas": matriz[1, 1],
            "precision": round(precision_score(objetivo, prediccion), 3),
            "recall": round(recall_score(objetivo, prediccion), 3),
            "f1": round(f1_score(objetivo, prediccion), 3),
        })
    tabla = pd.DataFrame(filas)
    return tabla.set_index("modelo")


# Paso 32. Curva ROC en prueba
def graficar_curvas_roc(modelos: dict[str, Pipeline], predictoras: pd.DataFrame, objetivo: pd.Series, titulo: str) -> None:
    """Dibuja en un solo gráfico la curva ROC de cada modelo sobre los datos de prueba."""
    plt.figure(figsize=(7, 6))
    panel = plt.gca()
    numero_modelo = 0
    for nombre in modelos:
        color = COLORES_MODELOS[numero_modelo]
        RocCurveDisplay.from_estimator(modelos[nombre], predictoras, objetivo, ax=panel, name=nombre, color=color, linewidth=2)
        numero_modelo = numero_modelo + 1
    panel.plot([0, 1], [0, 1], linestyle="--", color="#9e9e9e", linewidth=1, label="Azar (AUC = 0.50)")
    panel.set_xlabel("tasa de falsas alarmas")
    panel.set_ylabel("tasa de cancelaciones detectadas")
    panel.set_title(titulo)
    panel.legend(loc="lower right")
    plt.show()


# Paso 33. Importancia de las variables
def calcular_importancia(modelo: Pipeline, predictoras: pd.DataFrame, objetivo: pd.Series) -> pd.DataFrame:
    """Mide cuánto cae el F1 al desordenar al azar cada variable; mientras más cae, más aporta."""
    resultado = permutation_importance(
        modelo, predictoras, objetivo, scoring="f1",
        n_repeats=REPETICIONES_PERMUTACION, random_state=SEMILLA, n_jobs=-1,
    )
    importancia = pd.DataFrame(
        {"caida_f1": resultado.importances_mean, "variacion": resultado.importances_std},
        index=predictoras.columns,
    )
    importancia = importancia.sort_values("caida_f1", ascending=False)
    return importancia.round(4)


def graficar_importancia(importancia: pd.DataFrame, titulo: str) -> None:
    """Dibuja una barra horizontal por variable: mientras más larga, más aporta; en gris las de aporte menor que el mínimo."""
    ordenada = importancia.sort_values("caida_f1")   # de menor a mayor, para que la más importante quede arriba

    colores = []
    for valor in ordenada["caida_f1"]:
        if valor >= APORTE_MINIMO:
            colores.append(COLOR_BARRAS)
        else:
            colores.append(COLOR_BAJO_APORTE)

    plt.figure(figsize=(10, 0.4 * len(ordenada) + 1.5))
    barras = plt.barh(ordenada.index, ordenada["caida_f1"], color=colores)
    plt.bar_label(barras, fmt="%.4f", fontsize=8, padding=3)
    plt.xlabel("importancia (caída del F1 al desordenar la variable)")
    plt.title(titulo)
    plt.legend(handles=[
        Patch(color=COLOR_BARRAS, label="aporta a la predicción"),
        Patch(color=COLOR_BAJO_APORTE, label=f"aporte menor que {APORTE_MINIMO}"),
    ], loc="lower right")
    plt.tight_layout()
    plt.show()


# Paso 39. Variables de bajo aporte que se quitan en el Experimento 3
def elegir_variables_bajo_aporte(importancia: pd.DataFrame) -> list[str]:
    """Devuelve las variables cuyo aporte es menor que el mínimo, que se quitan en el Experimento 3."""
    variables = []
    for variable in importancia.index:
        if importancia.loc[variable, "caida_f1"] < APORTE_MINIMO:
            variables.append(variable)
    return variables
