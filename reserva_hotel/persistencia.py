"""Carga del modelo entrenado."""
import os

import joblib
import sklearn

from reserva_hotel.configuracion import NOMBRES_MODELOS


def existe_modelo(ruta_modelo: str) -> bool:
    """Indica si está el archivo del modelo que exporta el notebook."""
    return os.path.exists(ruta_modelo)


def cargar_modelo(ruta: str) -> dict:
    """Carga el paquete del modelo: el pipeline, sus predictoras, el umbral y la versión de scikit-learn."""
    return joblib.load(ruta)


def obtener_nombre_modelo(paquete: dict) -> str:
    """Devuelve el nombre en español del modelo que va al final del pipeline."""
    tipo_modelo = type(paquete["modelo"].steps[-1][1]).__name__
    if tipo_modelo in NOMBRES_MODELOS:
        return NOMBRES_MODELOS[tipo_modelo]
    return tipo_modelo


def version_compatible(paquete: dict) -> bool:
    """Indica si la versión de scikit-learn instalada es la misma con que se entrenó el modelo."""
    return paquete["version_sklearn"] == sklearn.__version__


def obtener_opciones(paquete: dict) -> dict[str, list[str]]:
    """Devuelve, para cada variable categórica, las categorías que el modelo vio al entrenar."""
    preparacion = paquete["modelo"].named_steps["preparacion"]
    codificador = preparacion.named_transformers_["categoricas"]
    columnas_categoricas = preparacion.transformers_[0][2]

    opciones = {}
    posicion = 0
    for columna in columnas_categoricas:
        categorias = []
        for categoria in codificador.categories_[posicion]:
            categorias.append(str(categoria))
        opciones[columna] = categorias
        posicion = posicion + 1
    return opciones
