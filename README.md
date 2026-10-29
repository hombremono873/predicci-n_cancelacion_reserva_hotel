# Predicción de cancelaciones de reservas hoteleras

**Abrir la aplicación en línea: https://prediccion-cancelacion-reserva-hotel.streamlit.app/**

No requiere instalar nada: funciona desde el navegador del computador o del celular.

Proyecto de minería de datos que estima la probabilidad de que una reserva hotelera sea cancelada. Tiene dos partes: un notebook de Google Colab con todo el análisis (exploración, limpieza, modelado y exportación del modelo) y una aplicación web en Streamlit que usa el modelo entrenado para calcular el riesgo de cancelación de una reserva.

## Contexto

Las cancelaciones dejan habitaciones vacías y causan pérdida de ingresos. En los datos usados, el **27,7 %** de las reservas se cancela. Saber qué reservas tienen riesgo alto le permite al hotel confirmar con el cliente, ajustar la sobreventa o pedir garantías.

- **Datos**: Hotel Booking Demand (Kaggle), 119.390 reservas de un hotel urbano y un hotel resort en Portugal, entre 2015 y 2017.
- **Variable objetivo**: target_cancelada (1 si la reserva se canceló, 0 si no).

## Resultados

Se compararon tres modelos (regresión logística, Random Forest y Gradient Boosting) en tres experimentos: con el mes de llegada, con la semana de llegada y sin las variables de menor aporte. El elegido fue **Gradient Boosting del Experimento 3**:

| Medida | Valor |
|---|---|
| Variables predictoras | 21 |
| F1 en prueba | 0,707 |
| AUC | 0,903 |
| Sobreajuste | No (diferencia de F1 entre entrenamiento y prueba menor que 0,05) |

## Estructura del repositorio

| Archivo o carpeta | Contenido |
|---|---|
| Diego_Jorge_Omar_Reserva_Hotel_Backup.ipynb | Notebook del proyecto (50 pasos), pensado para Google Colab |
| modelos/modelo_cancelaciones.joblib | Modelo entrenado que usa la aplicación |
| app.py | Punto de entrada de la aplicación Streamlit |
| reserva_hotel/ | Código de la aplicación: configuración, transformación de la reserva, predicción e interfaz |
| .streamlit/config.toml | Tema visual de la aplicación |
| requirements.txt | Librerías y versiones que necesita la aplicación |

## El notebook

Todo el código está dentro del notebook, así que no necesita archivos adicionales. Está organizado en 50 pasos:

| Pasos | Etapa | Qué se hace |
|---|---|---|
| 1 a 3 | Extracción | Librerías, constantes del proyecto y descarga del dataset desde Kaggle |
| 4 a 15 | Exploración | Renombrado al español, nulos, duplicados, distribuciones, asimetría y correlación |
| 16 a 24 | Limpieza y transformación | Duplicados, columnas con fuga de datos, valores imposibles, imputación, indicadores, transformaciones y validación |
| 25 | Carga | Guardado del dataset limpio en un archivo CSV |
| 26 a 46 | Modelado | División en entrenamiento y prueba, tres experimentos con tres modelos y comparación final |
| 47 a 50 | Exportación | Elección, guardado y descarga del mejor modelo, y una función main con todo el flujo |

### Ejecutarlo en Google Colab

1. Abrir https://colab.research.google.com y subir **Diego_Jorge_Omar_Reserva_Hotel_Backup.ipynb** (menú Archivo, Subir notebook).
2. Ejecutar todas las celdas en orden (menú Entorno de ejecución, Ejecutar todas). El dataset se descarga solo desde Kaggle.
3. Al final se descarga **modelo_cancelaciones.joblib**. Para usarlo en la aplicación, se copia en la carpeta **modelos** del proyecto.

El modelo solo carga con la misma versión de scikit-learn con que se entrenó (1.6.1). Antes de reemplazar el modelo de la aplicación, conviene revisar la tabla de versiones del Paso 48.

## La aplicación

La aplicación no vuelve a entrenar el modelo. Usa dos cosas del notebook:

- **El modelo entrenado** (modelos/modelo_cancelaciones.joblib), que incluye la preparación de las variables categóricas.
- **Las transformaciones de los pasos 21 a 23** (indicadores, logaritmo y raíz cuadrada, y codificación del mes y del régimen de comidas), copiadas en reserva_hotel/transformacion.py. Si se cambian en el notebook, hay que cambiarlas también allí.

### Uso

- **Portada**: presenta el proyecto y los créditos. El botón **Continuar** abre la aplicación.
- **Menú lateral**: permite cargar una reserva de ejemplo (riesgo bajo, medio o alto; son reservas reales del dataset) que llena todo el formulario, elegir el umbral de riesgo alto y ver qué modelo se usa.
- **Predicción**: un campo por cada una de las 21 predictoras del modelo, con el mismo nombre de la variable, agrupados en cuatro pestañas (Llegada y estancia, Reserva, Canal de venta, Cliente). Los rangos y las opciones salen de los datos limpios, y solo se ofrecen las combinaciones de segmento y canal que existen en ellos. La tarjeta de resultado muestra la probabilidad de cancelación y el nivel de riesgo, y se actualiza con cada cambio.
- **Cómo funciona**: explica qué datos usa el modelo, cómo leer el resultado y sus limitaciones.

El riesgo es **bajo** por debajo del promedio de cancelación de los datos (27,7 %), **medio** entre ese promedio y el umbral, y **alto** desde el umbral (50 % por defecto).

### Ejecutarla en el computador

Se necesita Python 3.13.

```
python -m venv entorno
entorno\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

En macOS o Linux, el segundo comando es **source entorno/bin/activate**. La aplicación se abre en el navegador en http://localhost:8501.

### Publicación en Streamlit Community Cloud

La aplicación está publicada en https://prediccion-cancelacion-reserva-hotel.streamlit.app/ y se actualiza sola cada vez que se sube un cambio a la rama main.

Para publicarla en otra cuenta:

1. Entrar a https://share.streamlit.io e iniciar sesión con la cuenta de GitHub dueña del repositorio.
2. Pulsar **Create app** y elegir la opción de desplegar desde un repositorio de GitHub.
3. Completar los datos: el repositorio, la rama **main** y el archivo principal **app.py**.
4. En **Advanced settings**, elegir **Python 3.13**.
5. Pulsar **Deploy**. La primera vez tarda unos minutos mientras instala las librerías de requirements.txt.

## Descargar el repositorio

El código está en https://github.com/hombremono873/predicci-n_cancelacion_reserva_hotel

Se puede descargar con el botón **Code** y luego **Download ZIP**, o clonarlo con git:

```
git clone https://github.com/hombremono873/predicci-n_cancelacion_reserva_hotel.git
cd predicci-n_cancelacion_reserva_hotel
```

## Créditos

- Universidad Santo Tomás
- Maestría en Análisis de Datos y Sistemas Inteligentes
- Estudiantes: Omar Alberto Torres, Diego Alejandro Roa Lara y Jorge Enrique Alvarez Martinez
- Docente: Gerardo Humberto Valencia Rivera
- Noviembre de 2026
