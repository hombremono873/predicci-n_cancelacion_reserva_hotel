"""Comparación de experimentos, elección, guardado y descarga del mejor modelo, y flujo completo con main()."""
import os
import platform

import joblib
import pandas as pd
import sklearn
from sklearn.pipeline import Pipeline

from constantes import (
    COLUMNAS_A_ELIMINAR, COLUMNAS_EXCLUIDAS_EXPERIMENTO_1, COLUMNAS_EXCLUIDAS_EXPERIMENTO_2,
    LIBRERIAS_APLICACION, RUTA_DATOS_LIMPIOS, RUTA_MODELO, UMBRAL_DECISION, UMBRAL_SOBREAJUSTE,
)
from exploracion import descargar_datos, leer_datos, renombrar_columnas
from limpieza import (
    eliminar_duplicados, eliminar_columnas, eliminar_filas_invalidas, imputar_nulos, corregir_categorias,
    crear_indicadores, transformar_colas_largas, codificar_ordinales, validar_limpieza, guardar_datos,
)
from modelado import (
    dividir_datos, elegir_predictoras, crear_modelos, entrenar_modelos, evaluar_modelos, calcular_importancia,
    elegir_variables_bajo_aporte,
)

# Descarga de archivos al computador, disponible solo en Colab
try:
    from google.colab import files as archivos_colab
except ImportError:
    archivos_colab = None


# Paso 44. Comparación de todos los modelos de los tres experimentos
def comparar_experimentos(experimentos: dict[str, dict]) -> pd.DataFrame:
    """Reúne las métricas de prueba de todos los modelos de todos los experimentos, ordenadas por F1 y AUC."""
    filas = []
    for nombre_experimento in experimentos:
        experimento = experimentos[nombre_experimento]
        for nombre_modelo in experimento["metricas"]:
            tabla = experimento["metricas"][nombre_modelo]
            filas.append({
                "experimento": nombre_experimento,
                "modelo": nombre_modelo,
                "predictoras": len(experimento["predictoras"]),
                "precision": tabla.loc["precision", "prueba"],
                "recall": tabla.loc["recall", "prueba"],
                "f1": tabla.loc["f1", "prueba"],
                "auc": tabla.loc["auc", "prueba"],
                "diferencia_f1": tabla.loc["f1", "diferencia"],
            })
    comparacion = pd.DataFrame(filas)
    comparacion = comparacion.set_index(["experimento", "modelo"])
    return comparacion.sort_values(["f1", "auc"], ascending=False)


# Paso 45. Versiones del entorno
def obtener_versiones() -> pd.DataFrame:
    """Muestra la versión de Python y de cada librería que necesita la aplicación."""
    versiones = {"python": platform.python_version()}
    for nombre in LIBRERIAS_APLICACION:
        versiones[nombre] = LIBRERIAS_APLICACION[nombre].__version__
    return pd.DataFrame({"version": versiones})


# Paso 46. Elección, guardado y descarga del mejor modelo
def guardar_modelo(modelo: Pipeline, predictoras: list[str], ruta: str) -> None:
    """Guarda el pipeline entrenado con sus predictoras, su umbral de decisión y la versión de scikit-learn."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    paquete = {
        "modelo": modelo,
        "predictoras": predictoras,
        "umbral": UMBRAL_DECISION,
        "version_sklearn": sklearn.__version__,
    }
    joblib.dump(paquete, ruta)
    print("Modelo guardado en:", os.path.abspath(ruta))


def descargar_archivo(ruta: str) -> None:
    """En Colab descarga el archivo a la carpeta de descargas del computador; fuera de Colab ya queda en la carpeta de trabajo."""
    if archivos_colab is None:
        print("Fuera de Colab, el archivo ya está en la carpeta de trabajo:", ruta)
        return
    archivos_colab.download(ruta)


def elegir_mejor_modelo(tabla_experimentos: pd.DataFrame) -> tuple[str, str]:
    """Devuelve el experimento y el modelo con mayor F1 en prueba entre los que no tienen sobreajuste."""
    sin_sobreajuste = tabla_experimentos[tabla_experimentos["diferencia_f1"] <= UMBRAL_SOBREAJUSTE]
    return sin_sobreajuste["f1"].idxmax()   # fila con el F1 más alto: (experimento, modelo)


# Paso 47. Función main: ejecución de todo el flujo
def ejecutar_experimento(
    columnas: list[str], columnas_excluidas: list[str], conjuntos: dict[str, tuple[pd.DataFrame, pd.Series]],
) -> dict:
    """Entrena los tres modelos con las predictoras de un experimento y calcula sus métricas sin mostrarlas."""
    predictoras = elegir_predictoras(columnas, columnas_excluidas)
    predictoras_entrenamiento, objetivo_entrenamiento = conjuntos["entrenamiento"]
    modelos = entrenar_modelos(crear_modelos(predictoras), predictoras_entrenamiento, objetivo_entrenamiento)
    return {
        "predictoras": predictoras,
        "modelos": modelos,
        "metricas": evaluar_modelos(modelos, conjuntos, mostrar=False),
    }


def main() -> None:
    """Ejecuta el flujo completo: ETL, experimentos, elección y descarga del mejor modelo."""
    # E: Extracción
    datos_originales = leer_datos(descargar_datos())

    # T: Transformación
    datos_renombrados = renombrar_columnas(datos_originales)
    datos_sin_duplicados = eliminar_duplicados(datos_renombrados)
    datos_sin_fugas = eliminar_columnas(datos_sin_duplicados, COLUMNAS_A_ELIMINAR)
    datos_validos = eliminar_filas_invalidas(datos_sin_fugas)
    datos_imputados = imputar_nulos(datos_validos)
    datos_corregidos = corregir_categorias(datos_imputados)
    datos_con_indicadores = crear_indicadores(datos_corregidos)
    datos_transformados = transformar_colas_largas(datos_con_indicadores)
    datos_limpios = codificar_ordinales(datos_transformados)
    validar_limpieza(datos_limpios)

    # L: Carga
    guardar_datos(datos_limpios, RUTA_DATOS_LIMPIOS)

    # Modelado: tres experimentos
    predictoras_entrenamiento, predictoras_prueba, objetivo_entrenamiento, objetivo_prueba = dividir_datos(datos_limpios)
    conjuntos = {
        "entrenamiento": (predictoras_entrenamiento, objetivo_entrenamiento),
        "prueba": (predictoras_prueba, objetivo_prueba),
    }
    columnas = list(predictoras_entrenamiento.columns)
    experimento_1 = ejecutar_experimento(columnas, COLUMNAS_EXCLUIDAS_EXPERIMENTO_1, conjuntos)
    experimento_2 = ejecutar_experimento(columnas, COLUMNAS_EXCLUIDAS_EXPERIMENTO_2, conjuntos)

    importancia_1 = calcular_importancia(
        experimento_1["modelos"]["Gradient Boosting"],
        predictoras_entrenamiento[experimento_1["predictoras"]], objetivo_entrenamiento,
    )
    variables_quitadas = elegir_variables_bajo_aporte(importancia_1)
    experimento_3 = ejecutar_experimento(columnas, COLUMNAS_EXCLUIDAS_EXPERIMENTO_1 + variables_quitadas, conjuntos)

    experimentos = {
        "1. Con mes": experimento_1,
        "2. Con semana": experimento_2,
        "3. Sin bajo aporte": experimento_3,
    }

    # Elección del mejor modelo
    tabla_experimentos = comparar_experimentos(experimentos)
    nombre_experimento, nombre_modelo = elegir_mejor_modelo(tabla_experimentos)
    print(f"Mejor modelo: {nombre_modelo} del experimento {nombre_experimento}")

    # Exportación del mejor modelo
    mejor_modelo = experimentos[nombre_experimento]["modelos"][nombre_modelo]
    predictoras_mejor_modelo = experimentos[nombre_experimento]["predictoras"]
    guardar_modelo(mejor_modelo, predictoras_mejor_modelo, RUTA_MODELO)
    descargar_archivo(RUTA_MODELO)


if __name__ == "__main__":
    main()
