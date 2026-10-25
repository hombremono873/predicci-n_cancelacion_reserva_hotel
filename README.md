# Predicción de cancelaciones de reservas hoteleras

**Abrir la aplicación en línea: https://prediccion-cancelacion-reserva-hotel.streamlit.app/**

No requiere instalar nada: funciona desde el navegador del computador o del celular.

Proyecto de minería de datos que estima la probabilidad de que una reserva hotelera sea cancelada. Incluye el análisis completo en un notebook (exploración, limpieza, modelado y exportación del modelo) y una aplicación web en Streamlit para consultar el riesgo de cancelación de una reserva.

## Contexto

Las cancelaciones generan habitaciones vacías y pérdida de ingresos. En los datos usados, el **27,7 %** de las reservas se cancela. Anticipar qué reservas tienen riesgo alto permite al hotel confirmar con el cliente, ajustar la sobreventa o pedir garantías.

- **Datos**: Hotel Booking Demand (Kaggle), reservas de un hotel de ciudad y un hotel de playa en Portugal entre 2015 y 2017.
- **Variable objetivo**: target_cancelada (1 si la reserva se canceló, 0 si no).

## Resultados

Se compararon nueve modelos en tres experimentos (con mes, con semana y sin las variables de bajo aporte). El mejor fue **Gradient Boosting del Experimento 3**:

| Medida | Valor |
|---|---|
| Variables predictoras | 21 |
| F1 en prueba | 0,707 |
| AUC | 0,903 |
| Sobreajuste | No (diferencia de F1 entre entrenamiento y prueba menor que 0,05) |

## Estructura del repositorio

| Archivo o carpeta | Contenido |
|---|---|
| ReservaHotel.ipynb | Notebook principal (47 pasos), pensado para Google Colab |
| ReservaHotelBackup.ipynb | Versión anterior del notebook, con todo el código en las celdas |
| constantes.py | Constantes del proyecto |
| exploracion.py | Descarga, lectura y análisis exploratorio |
| limpieza.py | Duplicados, fugas de información, valores imposibles, imputación y transformaciones |
| modelado.py | División de los datos, pipelines, métricas e importancia de las variables |
| exportacion.py | Comparación de modelos, elección del mejor y guardado |
| modelos/modelo_cancelaciones.joblib | Modelo entrenado que usa la aplicación |
| app.py | Punto de entrada de la aplicación Streamlit |
| reserva_hotel/ | Código de la aplicación (configuración, transformación, predicción e interfaz) |
| .streamlit/config.toml | Tema visual de la aplicación |
| requirements.txt | Librerías y versiones necesarias |

## Acceso al repositorio en GitHub

El código está en:

https://github.com/hombremono873/predicci-n_cancelacion_reserva_hotel

Para descargarlo se puede usar el botón **Code** y luego **Download ZIP**, o clonarlo con git:

```
git clone https://github.com/hombremono873/predicci-n_cancelacion_reserva_hotel.git
cd predicci-n_cancelacion_reserva_hotel
```

## Ejecutar el notebook en Google Colab

1. Abrir https://colab.research.google.com y subir **ReservaHotel.ipynb** (menú Archivo, Subir notebook).
2. En el panel **Archivos** de Colab, subir constantes.py, exploracion.py, limpieza.py, modelado.py y exportacion.py.
3. Ejecutar todas las celdas en orden. El dataset se descarga solo desde Kaggle con kagglehub.
4. Al final se descarga **modelo_cancelaciones.joblib**, que es el que usa la aplicación.

Si se modifica alguno de los archivos .py, hay que reiniciar la sesión de Colab para que tome los cambios.

## Ejecutar la aplicación en el computador

Se necesita Python 3.13.

```
python -m venv entorno
entorno\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

En macOS o Linux, el segundo comando es **source entorno/bin/activate**. La aplicación se abre en el navegador en http://localhost:8501.

## Publicar la aplicación en Streamlit Community Cloud

Streamlit Community Cloud publica gratis aplicaciones que están en un repositorio público de GitHub.

1. Entrar a https://share.streamlit.io e iniciar sesión con la cuenta de GitHub dueña del repositorio.
2. Pulsar **Create app** y elegir la opción de desplegar desde un repositorio de GitHub.
3. Completar los datos:
   - **Repository**: hombremono873/predicci-n_cancelacion_reserva_hotel
   - **Branch**: main
   - **Main file path**: app.py
   - **App URL**: el nombre que se quiera para la dirección, por ejemplo cancelaciones-hotel (queda como cancelaciones-hotel.streamlit.app).
4. En **Advanced settings**, elegir **Python 3.13**, la misma versión con la que se entrenó y probó el modelo.
5. Pulsar **Deploy**. La primera vez tarda unos minutos mientras instala las librerías de requirements.txt.

Cada vez que se sube un cambio a la rama main, la aplicación se actualiza sola.

**Dirección de la aplicación publicada**: https://prediccion-cancelacion-reserva-hotel.streamlit.app/

## Uso de la aplicación

- **Portada**: presenta el proyecto y los créditos. El botón **Continuar** abre la aplicación.
- **Predicción**: los datos de la reserva se llenan en cuatro pestañas (Llegada, Huéspedes, Canal y cliente, Historial). La tarjeta de resultado muestra la probabilidad de cancelación y el nivel de riesgo, y se actualiza con cada cambio.
- **Cómo funciona**: explica cómo se calcula el riesgo.
- **Menú lateral**: permite cargar reservas de ejemplo, ajustar el umbral de riesgo alto y ver la ficha del modelo.

El riesgo es **alto** cuando la probabilidad llega al umbral, **medio** cuando está entre el promedio del hotel (27,7 %) y el umbral, y **bajo** cuando está por debajo del promedio.

## Créditos

- Universidad Santo Tomás
- Maestría en Análisis de Datos y Sistemas Inteligentes
- Estudiantes: Omar Alberto Torres y Diego Alejandro Roa Lara
- Docente: Gerardo Humberto Valencia Rivera
- Noviembre de 2026
