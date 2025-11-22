# 🖼️ 1. Análisis de Sentimientos por Imágenes con MediaPipe, Hilos, Mutex y Semáforos

Este componente implementa un sistema de clasificación de **emociones básicas** (feliz, triste, enojado) a partir de imágenes faciales. Para la detección y extracción de características, se utiliza la librería **MediaPipe Face Mesh**.

El procesamiento es **paralelo**, donde cada imagen se analiza en un **hilo independiente**, y el acceso a recursos compartidos se sincroniza mediante `Lock` y `Semaphore`.

---

### 🎯 Objetivo de la Sección

Desarrollar un sistema concurrente capaz de:

1.  **Detectar rostros** en imágenes usando **MediaPipe Face Mesh**.
2.  **Extraer *landmarks*** faciales relevantes (puntos clave). 
3.  **Inferir el sentimiento** (feliz, triste, enojado) utilizando reglas geométricas simples basadas en los *landmarks* extraídos.
4.  **Procesar múltiples imágenes simultáneamente** mediante hilos para optimizar el rendimiento.

| Mecanismo de Concurrencia | Propósito |
| :--- | :--- |
| **Hilos** (`threading.Thread`) | Procesamiento de cada imagen en paralelo. |
| **Mutex** (`Lock`) | Proteger la estructura de resultados compartida. |
| **Semáforo** (`Semaphore`) | Limitar el número de imágenes procesadas al mismo tiempo, controlando la carga del sistema. |

### ⚙️ Instalación y Ejecución

Las dependencias principales para este entregable son
- opencv-python
- mediapipe
- numpy


## Esquema de Procesamiento Paralelo

| Etapa 1: Entrada | Etapa 2: Procesamiento (Hilos Paralelos) | Etapa 3: Salida Unificada |
| :---: | :---: | :---: |
| **[Imagen A]** | $\rightarrow$ **[Hilo 1]** | \ |
| **[Imagen B]** | $\rightarrow$ **[Hilo 2]** | $\rightarrow$ **[Resultados finales protegidos con Lock]** |
| **[Imagen C]** | $\rightarrow$ **[Hilo 3]** | / |

---
### 🧠 Lógica del Procesamiento

La clasificación de emociones se basa en el análisis de *landmarks* faciales extraídos por MediaPipe, siguiendo una serie de pasos concurrentes:

---

- #### 1. Detección del Rostro

Se utiliza la solución de **MediaPipe Face Mesh** para identificar la posición y los 468 *landmarks* (puntos clave) del rostro en la imagen:

```bash
mp.solutions.face_mesh.FaceMesh
```
-Regla de Salida: Si el proceso no detecta un rostro en la imagen de entrada, el resultado inmediato es: “SIN ROSTRO DETECTADO”.

- #### 2. Landmarks Utilizados para Clasificación

Para inferir la emoción, el sistema se enfoca en las métricas geométricas de las siguientes áreas faciales, ya que son las más expresivas de las emociones básicas:

    Comisuras de la boca

    Apertura y curvatura de la boca

    Ángulo de inclinación de las cejas

    Relación vertical entre los labios
    
#### 3. Reglas de Sentimientos (Clasificación Básica)

La inferencia de la emoción se realiza aplicando **reglas geométricas simples** (umbrales) sobre los *landmarks* extraídos.

| Emoción | Patrón Geométrico (Resumen) |
| :--- | :--- |
| **Feliz** | Boca más ancha que alta, con **comisuras elevadas** (arqueadas hacia arriba). |
| **Triste** | Boca angosta y **comisuras caídas** (arqueadas hacia abajo). |
| **Enojado** | **Ojos entrecerrados** y **cejas inclinadas** hacia el centro (fruncidas). |


- ### 🧵 Concurrencia Implementada

Los mecanismos de concurrencia aseguran que el análisis intensivo de imágenes (MediaPipe) se ejecute de forma **paralela y segura**. 

| Mecanismo | Código de Implementación | Función |
| :--- | :--- | :--- |
| **✔ Creación de Hilos** | `t = threading.Thread(target=procesar_imagen, args=(ruta,))`<br>`t.start()` | Cada imagen de entrada lanza un **hilo independiente** para su procesamiento. |
| **✔ Semáforo** | `semaforo = Semaphore(2)` | Limita el procesamiento a un máximo de **2 hilos** (imágenes) simultáneamente, evitando la saturación del sistema. |
| **✔ Mutex** | `with lock:`<br>`resultados[ruta] = emocion` | Protege el **diccionario de resultados** (`resultados`), previniendo que múltiples hilos escriban o corrompan los datos al mismo tiempo (**condición de carrera**). |

####  Ejecución

Para iniciar la aplicación 
```bash
python "nombre".py
```
(Se deben tener preparadas las imagenes dentro de la carpeta para que logre procesarlas)

- #### 📊 Ejemplo de Salida

```bash
Imagen_feliz.jpg   →   Feliz
rostro_3.jpg       →   Enojado
selfie.png         →   SIN ROSTRO DETECTADO
```

- #### ✔ Estado final de la sección

La solución completa incluye:

Procesamiento por hilos ✔

Uso de semáforo ✔

Protección con mutex ✔

MediaPipe para detección facial ✔

Clasificación de tres emociones (feliz, triste, enojado) ✔

---

![Image](https://github.com/user-attachments/assets/22ef69cf-dfdb-4cf8-b313-75174b84a129)

![Image](https://github.com/user-attachments/assets/fc167f04-2245-4811-a680-85c0e4c9023f)


---

# 2) 📘 Desarrollo de un ETL partiendo de una base de datos

---

### 🎯 Objetivo del Punto 2

El objetivo es desarrollar un pipeline ETL funcional, entrenar un modelo simple y desplegar un dashboard interactivo en Streamlit, integrando diferentes conceptos del curso.

Específicamente, se busca:

* Desarrollar un **ETL completo** a partir de la base de datos proporcionada en clase (o datos sintéticos en caso de ausencia).
* Aplicar **transformaciones**, generar un dataset procesado.
* Construir un **dashboard con Streamlit** que visualice la información obtenida y los resultados del modelo.
  
### 📊 Descripción del Dashboard (Resumen Funcional)

- El dashboard desarrollado en este punto ofrece una interfaz interactiva que permite visualizar y analizar los datos resultantes del proceso ETL. Entre sus funcionalidades principales se encuentran:

    - Visualización del dataset procesado: muestra las primeras filas del archivo procesado.csv, permitiendo revisar el estado final de los datos después de la limpieza y transformación.

    - Mapa de correlación: genera una matriz gráfica interactiva que permite identificar relaciones entre las variables numéricas del conjunto de datos.

    - Exploración de distribuciones: ofrece la posibilidad de seleccionar cualquier variable numérica y visualizar su distribución mediante un histograma.

    - Predicción con el modelo entrenado: permite cargar automáticamente el modelo generado en el entrenamiento y realizar una predicción utilizando la primera fila del dataset, mostrando el valor calculado en la interfaz         lateral.

    - Indicadores de estado: el dashboard valida la presencia del dataset procesado y del modelo entrenado, mostrando advertencias si alguno de ellos no está disponible.

    - Este panel integra de forma práctica el resultado del ETL, el modelo de predicción y las herramientas de visualización, permitiendo analizar el comportamiento del sistema STC de manera clara e interactiva.


#### Conceptos Integrados

Este punto integra y refuerza conceptos clave vistos a lo largo del laboratorio:

* Terminal de **Ubuntu Linux**
* **Concurrencia / hilos / semáforos**
* **Seguridad en la red** (nmap, lynis)
* **Entornos virtuales** (`venv`)
* **Docker** para despliegue
* Uso de librerías como Mediapipe y PyBullet (conceptos relacionados a visión/simulación)
* **Arquitectura modular** en Python

---

### 📌 Descripción del Trabajo Realizado

Durante este punto del laboratorio se desarrolló una solución modular, compuesta por un pipeline de datos y una capa de visualización:

## 🧹 Explicación Detallada del Proceso ETL Realizado

Este apartado responde a la pregunta del profesor sobre **“qué se hizo con los datos, cómo se limpiaron y qué criterios se aplicaron en el procesamiento”**.

---

### 1. ¿Qué datos contenía la base original?

La base de datos (archivo Excel de la tesis **“Síndrome de Túnel Carpiano”**) contenía:

* **Señales capturadas por sensores** (EMG, fuerza, acelerómetros, etc.).
* Información de **participantes**.
* Registros por **ensayo**.
* **Tiempos y valores** por cada movimiento.
* **Etiquetas** del experimento (**normal / patológico**).

> El archivo estaba dividido en **varias hojas** y tenía **formatos no uniformes**.

---

## 📌 2. Principales problemas encontrados en la base de datos cruda

Durante la implementación del ETL se identificaron varios *issues* típicos:

* **❌ Formato inconsistente**
    * Algunas hojas tenían encabezados distintos.
    * Los nombres de columnas no seguían un mismo patrón.
* **❌ Valores nulos o incompletos (`NaN`)**
    * En varias columnas de señales aparecían celdas vacías.
    * Registros incompletos por fallas en el sensor.
* **❌ Variables irrelevantes**
    * Había columnas que no aportaban al análisis (comentarios, códigos internos, *timestamps* redundantes).
* **❌ Datos numéricos sin normalizar**
    * Rango de sensores distinto entre pruebas.
    * Señales sin escalar: **impedían modelos de ML**.

---

## 📌 3. E — Extract (Extracción)

El script de ETL realizó los siguientes pasos de extracción:

1.  **Leyó todas las hojas del Excel** usando `pandas.read_excel()`.
2.  **Unificó** los *datasets* en un solo `DataFrame`.
3.  **Extrajo únicamente las columnas relevantes**:
    * Señales fisiológicas
    * Fuerzas y aceleraciones
    * Etiqueta (diagnóstico)
    * ID del paciente

> Se construyó un solo *dataset* maestro llamado **`bd_completa`**.

## 📌 4. T — Transform (Transformación)

Las transformaciones aplicadas fueron:

- ✔ Limpieza de filas vacías
```bash
df = df.dropna()
```
- ✔ Corrección de tipos de datos

    - Se forzó a float32 todas las columnas de señales.

    - Se eliminaron columnas con strings innecesarios.

- ✔ Normalización MinMax por sensor

    - Esto es esencial para modelos neuronales:
```bash
scaler = MinMaxScaler()
df[numericas] = scaler.fit_transform(df[numericas])
```
- ✔ Renombrado coherente de columnas

    - Para evitar errores posteriores en el modelo.

- ✔ Eliminación de duplicados
```bash
df = df.drop_duplicates()
```
- ✔ Creación de una columna de índice normalizado

    - Facilita el acceso desde el dashboard.

## 📌 5. L — Load (Carga)

Finalmente, el ETL generó:
```bash
data/procesado.csv
```

- Este archivo es:

    - Limpio

    - Normalizado

    - Cohesivo

    - Consistente en nombres y tipos

    - Sin duplicados

    - Listo para análisis y para alimentar el modelo neuronal

El dashboard de Streamlit lo usa directamente.


#### ✔ 1. Un Pipeline ETL Completo

El pipeline se divide en tres módulos esenciales para el procesamiento de datos:

| Módulo | Función | Descripción |
| :--- | :--- | :--- |
| **`extract`** | **Carga de Datos** | Carga de datos desde archivos fuente (Excel/CSV) o generación de datos sintéticos. |
| **`transform`** | **Limpieza y Normalización** | Aplicación de reglas de negocio, limpieza de *outliers* y normalización de variables. |
| **`load`** | **Exportación** | Exportación del dataset transformado a un archivo `procesado.csv` para su uso posterior. |

El ETL se ejecuta mediante el siguiente comando:

```bash
python3 etl_pipeline.py
```

**✔ 2. Entrenamiento de un modelo básico**

Utilizando redes neuronales con Keras/TensorFlow:

- Normalización MinMaxScaler

- Red sencilla (64–32–1)

- Entrenamiento supervisado

- Guardado del modelo en model/modelo_exportado.h5

Se ejecuta con:

```bash
python3 model/train_model.py
```
**✔ 3. Creación del Dashboard en Streamlit**

El dashboard:

- Muestra el dataset procesado

- Genera un mapa de correlación

- Permite visualizar distribuciones

- Carga el modelo entrenado

- Realiza predicciones sobre filas del dataset

El dashboard se ejecuta con:
```bash
streamlit run dashboard/app.py
```

### 🧠 Conceptos aplicados
---

**🟦 Ubuntu Linux**

- Terminal, rutas absolutas y relativas

- Manejo de entornos virtuales

- Ejecución de scripts Python

- Instalación de librerías del laboratorio

**🟧 ETL**

- Separación en módulos: extract, transform, load

- Manejo de errores (archivos corruptos, rutas inválidas)

- Consolidación en procesado.csv

**🟨 Concurrencia, hilos y semáforos**

- Aunque no se aplican directamente al ETL, sí se integran en:

- Manejo de carga de modelo

**🟥 Seguridad en la red**
```bash
nmap -sV localhost
sudo lynis audit system
```
Aplicadas para:

- Evaluar seguridad del contenedor

- Revisar puertos expuestos del dashboard

**🟪 Docker**

- Se preparó un Dockerfile para permitir:

- Instalar dependencias

- Ejecutar ETL, modelo y dashboard dentro de un contenedor

**🟩 Machine Learning**

- Red neuronal artificial

- Normalización

- Entrenamiento supervisado

- Predicción desde el dashboard

**🟫 Mediapipe / PyBullet**

- Aunque no se usan directamente en el ETL, se relacionan con:

- Manejo de grandes volúmenes de datos sensoriales

- Comprensión de señales biomecánicas

- Aplicaciones del curso

- Lectura concurrente de archivos (concepto discutido)

- Estructura del dashboard

---

### 📂 Estructura del directorio

Descripción de Módulos

    - data/

        BD_COMPLETA.xlsx: Base de datos original (opcional).

        sensores_base.csv: Datos base (Generados sintéticamente).

        procesado.csv: Dataset limpio y transformado (Salida del ETL).

    - etl/

        extract.py: Módulo de Extracción (Carga de datos).

        transform.py: Módulo de Transformación (Limpieza y normalización).

        load.py: Módulo de Carga (Exporta a procesado.csv).

        run_etl.py: Script principal de ejecución del pipeline.

    - model/

        train_model.py: Script para el entrenamiento del modelo.

        predict_model.py: Script para predicciones.

        modelo_exportado.h5: Modelo entrenado y serializado.

    - dashboard/

        app.py: Dashboard interactivo con Streamlit (Punto 2).

    - tools/

        gen_synthetic.py: Script para generar datos sintéticos.
---

## 🚀 Procedimiento paso a paso

- 1️⃣ Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

- 2️⃣ Instalar dependencias

```bash
    pip install -r requirements.txt
```

- 3️⃣ Generar datos sintéticos (opcional)

```bash
    python3 tools/gen_synthetic.py
```

- 4️⃣ Ejecutar ETL completo

```bash
    python3 etl/run_etl.py
```
Se genera:
```bash
    data/procesado.csv
```

- 5️⃣ Entrenar el modelo
```bash
    python3 model/train_model.py
```
Se genera:
```bash
    model/modelo_exportado.h5
```
- 6️⃣ Ejecutar dashboard
```bash
    streamlit run dashboard/app.py
```

### 📊 Resultados esperados

- Archivo procesado.csv generado correctamente

- Modelo entrenado disponible

- Dashboard con:

    - visualización de la base procesada

    - mapa de correlación

    - histogramas

    - predicción con modelo neuronal

### 🧪 Validación adicional 

Ver puertos expuestos:
```bash
    nmap -sV localhost
```

Auditoría del sistema:
```bash
    sudo lynis audit system
```
--- 

# 🐳 Dockerización

Se realizó la **dockerización** del **ETL**, el **modelo** y el **dashboard** para garantizar **portabilidad**, **reproducibilidad** y **despliegue independiente** del sistema operativo.

A continuación se describe el proceso realizado.

---

### 📌 1. Creación del Dockerfile

Se creó un archivo `Dockerfile` en el directorio raíz del proyecto.

### ¿Qué hace este Dockerfile?

* Utiliza una **imagen ligera** (`python:3.12-slim`).
* Copia **todo el proyecto** al contenedor.
* Instala **dependencias** sin utilizar caché.
* Expone el **puerto 8501** (donde corre Streamlit).
* Arranca directamente el **Dashboard** al iniciar el contenedor.

###  2. Construcción de la imagen

Desde la carpeta raíz del proyecto:

```bash
    docker build -t stc_lab7 .
```
Donde:

- stc_lab7 es el nombre de la imagen resultante.

Esto genera una imagen autosuficiente que contiene:

- ETL

- Modelo

- Dashboard

- Dependencias de Python

-  3. Ejecución del contenedor

Para ejecutar el dashboard desde Docker

```bash
    docker run -p 8501:8501 stc_lab7
```
Descripción:

- -p 8501:8501 expone el puerto del contenedor al host

- El dashboard queda disponible en:
    ```bash
    http://localhost:8501
    ```
    
###  4. Verificación del despliegue

Después de levantar el contenedor:

✔ Ver puertos activos con nmap
  ```bash
    nmap -sV localhost
   ```

Debe aparecer:
 ```bash
    8501/tcp open http streamlit
 ```
    
✔ Auditoría de seguridad opcional con lynix
  ```bash
sudo lynis audit system
  ```

- Esto valida:

    - dependencias del contenedor

    - puertos expuestos

    - vulnerabilidades conocidas

--- 

![Image](https://github.com/user-attachments/assets/86ae9d71-2f22-4654-a537-7bd19c0706f5)

![Image](https://github.com/user-attachments/assets/4b555cdf-5e0a-4aa6-b504-0ecd36eadbba)

![Image](https://github.com/user-attachments/assets/24a32a3c-eba4-4868-adf3-b549920acd65)

![Image](https://github.com/user-attachments/assets/4b6b32cc-e72a-4871-9d68-f62025598b45)

![Image](https://github.com/user-attachments/assets/7cf7f106-0c90-4d19-b969-b73633a8f523)

![Image](https://github.com/user-attachments/assets/502d65a6-a3af-4552-ba56-ef0e6c926db4)

![Image](https://github.com/user-attachments/assets/6ad58cea-81cf-4d2e-ad3d-2adc54db6886)

![Image](https://github.com/user-attachments/assets/c160bbe4-4da1-416a-8a95-5ad446a19343)

![Image](https://github.com/user-attachments/assets/3d7fe27e-7889-4f8e-a006-d864758667a5)

---

# 🤖 Propuesta de Proyecto: Sistema Inteligente de Monitoreo Ambiental (SIMA)

------------

## a) Propuesta de Proyecto

El proyecto SIMA (Sistema Inteligente de Monitoreo Ambiental) busca abordar la problemática de la gestión y prevención de desastres ambientales (como inundaciones o deslizamientos) mediante la implementación de una infraestructura de IA robusta y descentralizada.

Utilizaremos el stack aprendido en Digitales III:

- Identificación y Localización: Se empleará YOLO (You Only Look Once), entrenado con OpenCV, para identificar en tiempo real patrones de riesgo en imágenes satelitales o de drones (e.g., cambios en el cauce de ríos, deforestación, grietas en el suelo).

- Contenedorización y Despliegue: La aplicación de IA, incluyendo el modelo YOLO y el servicio web, se empaquetará en contenedores Docker. Esto asegura la portabilidad y escalabilidad en la infraestructura de la convocatoria.

- Interfaz de Usuario: La visualización de alertas e información geográfica (mapas de calor de riesgo, ubicación de sensores) se realizará mediante una interfaz web desarrollada con Streamlit, facilitando la apropiación social del conocimiento por parte de las organizaciones locales.

- Control de Versiones y Colaboración: Todo el código fuente, modelos y documentación (README) se gestionarán en GitHub para garantizar la trazabilidad y la colaboración entre los actores de la alianza.

- Sistema Operativo Base: Se utilizará Ubuntu como sistema operativo en los servidores y entornos de desarrollo/despliegue, aprovechando su estabilidad y soporte en la comunidad de código abierto.

---

## 🌍 b) Sistema Inteligente de Monitoreo Ambiental (SIMA) - Convocatoria MinCiencias
### Infraestructura IA para la Resiliencia Territorial

[![Estado del Proyecto](https://img.shields.io/badge/Estado-En%20Desarrollo-blue)](README.md)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)

### 🚀 Resumen del Proyecto

SIMA es una solución de Inteligencia Artificial orientada a fortalecer la **resiliencia territorial** ante los desafíos del **cambio climático**. El proyecto propone una **infraestructura robusta** para el monitoreo predictivo de riesgos ambientales, transformando datos geoespaciales en alertas accionables.

| Componente Clave | Tecnología Principal | Propósito |
| :--- | :--- | :--- |
| **Visión por Computadora** | **YOLOv8** & **OpenCV** | Detección de anomalías y patrones de riesgo (e.g., deslizamientos, inundaciones). |
| **Infraestructura** | **Docker** & **Ubuntu** | Contenedorización para un despliegue ágil y escalable. |
| **Interfaz de Usuario** | **Streamlit** | Dashboard interactivo para la visualización de alertas y mapas de riesgo. |
| **Gestión de Código** | **GitHub** | Control de versiones, trazabilidad y colaboración académica/empresarial. |

---

### 🏛️ Arquitectura del Sistema

La arquitectura sigue un patrón modular y distribuido, ideal para la infraestructura de IA:

| Etapa | Módulo | Descripción |
| :---: | :---: | :--- |
| **1. Adquisición de Datos** | **Módulo Geo-Data** | Captura de imágenes satelitales (fuentes abiertas/públicas) y datos de sensores IoT. |
| **2. Procesamiento** | **Módulo de Preprocesamiento** | Normalización de imágenes y etiquetado de datos (usando scripts Python en **Ubuntu**). |
| **3. Inferencia IA** | **Módulo de Detección YOLO** | Contenedor **Docker** con el modelo **YOLO/OpenCV** para la identificación de riesgos. |
| **4. Alerta y Visualización** | **Módulo Streamlit** | Interfaz web que recibe las detecciones y las muestra en mapas georreferenciados. |

**Diagrama de Bloques Conceptual**

graph TD
    A[Datos Satelitales/IoT] --> B(Procesamiento de Datos);
    B --> C{Contenedor Docker: YOLO/OpenCV};
    C --> D(Base de Datos de Alertas);
    D --> E[Streamlit Dashboard];
    E --> F[Usuarios Finales/Organizaciones Locales];
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#ccf,stroke:#333,stroke-width:2px

**Nota:** Este diagrama conceptual de flujo de datos se implementará usando las capacidades de contenerización de **Docker**.

---

### ⚙️ Instrucciones de Despliegue (Docker y Ubuntu)

Para replicar este proyecto se requiere:

1.  Clonar el repositorio: `git clone https://github.com/tu-usuario/SIMA.git`
2.  Construir la imagen de Docker: `docker build -t sima-ia .`
3.  Ejecutar el contenedor en el servidor **Ubuntu**: `docker run -p 8501:8501 sima-ia`

El dashboard de **Streamlit** estará disponible en el puerto `8501`.

---
