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

### c) Tecnologías Futuras Sugeridas

Como experto en la temática y basándote en lo aprendido en Digitales III, estas son las tecnologías futuras que sugiero para llevar el proyecto a un nivel superior, enfocadas en la infraestructura de IA y la eficiencia:

1. Orquestación de Contenedores (Kubernetes - K8s):

- Por qué: Para gestionar un gran número de contenedores Docker en un entorno de producción (infraestructura a gran escala de MinCiencias). Permite la auto-sanación, el escalado automático de los módulos de inferencia (YOLO) y la gestión eficiente de recursos.

2. Modelos de Lenguaje de Gran Escala (LLM) con RAG para Asistencia en Desastres:

- Por qué: Integrar un LLM (entrenado con datos locales/regionales) con la arquitectura RAG (Retrieval-Augmented Generation). Esto permitiría a los usuarios (organizaciones locales) consultar la base de datos de alertas en lenguaje natural (ej. "¿Hay riesgo de inundación en el río X la próxima semana?").

3. Edge Computing y Microcontroladores para Sensores Remotos:

- Por qué: Implementar una versión muy ligera de la inferencia (Tiny-YOLO o modelos optimizados) directamente en dispositivos de bajo consumo (Raspberry Pi o ESP32) ubicados en zonas de riesgo, enviando solo las alertas críticas. Esto reduce la latencia y la dependencia de la conexión a la nube para la toma de decisiones críticas.

El siguiente video muestra la visión de MinCiencias sobre las convocatorias, lo que ayuda a contextualizar la importancia de la iniciativa Colombia Inteligente.

**https://www.youtube.com/watch?v=GlWUn2T3h5Y**

---

## 💡 d) Conclusión e Impacto Socio-Técnico

### Conclusión y Alineación

El Sistema Inteligente de Monitoreo Ambiental (SIMA) demuestra cómo las tecnologías aprendidas en Digitales III (OpenCV, YOLO, Streamlit, Docker, y GitHub) forman una infraestructura de IA coherente y desplegable. La selección de Docker es crucial, ya que garantiza la portabilidad de nuestro modelo (YOLO) a través de la infraestructura que la convocatoria de MinCiencias busca establecer, asegurando la repetibilidad y la escalabilidad del sistema en diversas regiones de Colombia.

---

### Impacto Social y Contribución a la Convocatoria

El proyecto SIMA impacta directamente la misión de la convocatoria "Colombia Inteligente: Infraestructura para el Desarrollo de la Inteligencia Artificial" al:

1. Fomentar la Apropiación Social: El uso de Streamlit permite crear un dashboard accesible que traduce la compleja detección de riesgos por IA en información simple para los tomadores de decisiones locales, cumpliendo con el objetivo de democratizar el acceso a la tecnología.

2. Mitigar Riesgos Ambientales: Al proporcionar alertas tempranas, el sistema reduce la vulnerabilidad de las comunidades ante eventos climáticos extremos, contribuyendo a la resiliencia territorial y salvaguardando vidas y bienes.

3. Generación de Datos: SIMA crea una fuente continua de datos etiquetados sobre patrones de riesgo, que puede ser utilizada por la infraestructura de MinCiencias para entrenar modelos de IA más robustos a nivel nacional.

En esencia, el proyecto no solo utiliza la infraestructura de IA, sino que contribuye activamente a ella, proporcionando una aplicación práctica y un modelo de datos valioso.
# 🛠️ Exploración de Tecnologías de Infraestructura y Automatización

Para que el proyecto SIMA trascienda el entorno local y se integre eficientemente en la infraestructura de IA de MinCiencias, es imperativo dominar herramientas de aprovisionamiento, configuración y mensajería.

## a) 🌍 Terraform: Infraestructura como Código (IaC)

Terraform, desarrollado por HashiCorp, es una herramienta agnóstica a la nube que permite a los equipos definir y aprovisionar la infraestructura de un centro de datos o de proveedores de nube (AWS, Azure, Google Cloud, OpenStack) mediante archivos de configuración declarativos.

| Característica Clave | Descripción | Beneficio para SIMA |
|----------------------|-------------|----------------------|
| Declarativo | Define el estado final deseado de la infraestructura (ej. "Quiero una máquina virtual, un bucket de almacenamiento y una red"). | Predecibilidad: Asegura que los entornos de desarrollo, prueba y producción sean idénticos, eliminando errores de configuración manual. |
| Proveedores | Soporta una vasta cantidad de providers (más de 1000) que van desde nubes públicas hasta servicios SaaS y soluciones on-premise (como OpenStack). | Portabilidad: Permite migrar o replicar el entorno de IA de SIMA (VMs, redes, balanceadores) en cualquier nube que se exija en la convocatoria. |
| Planificación | Utiliza los comandos `plan` y `apply`. El plan muestra exactamente qué recursos se crearán, modificarán o destruirán antes de ejecutar. | Seguridad: Permite revisar y auditar los cambios de infraestructura antes de aplicarlos, minimizando el riesgo de interrupciones o costos inesperados. |
| Lenguaje (HCL) | Utiliza el HashiCorp Configuration Language (HCL), que es legible por humanos y fácil de aprender. | Legibilidad: Facilita la colaboración y la revisión por pares del código de infraestructura. |

---

### b) ⚙️ Ansible: Automatización de la Configuración

Ansible, una herramienta de automatización open source mantenida por Red Hat, se enfoca en la gestión de la configuración, el despliegue de aplicaciones y la orquestación.

| Característica Clave | Descripción | Beneficio para SIMA |
|----------------------|-------------|----------------------|
| Agente Less | No requiere software o agentes especiales instalados en las máquinas gestionadas. Utiliza SSH para la comunicación (en sistemas Linux/Ubuntu) y PowerShell/WinRM (en Windows). | Simplicidad: Reduce la sobrecarga y los puntos de fallo, siendo ideal para configurar rápidamente el entorno Ubuntu de los servidores. |
| Playbooks (YAML) | Las tareas se definen en archivos YAML llamados Playbooks, que son fáciles de leer y escribir. | Claridad: Permite definir la secuencia de pasos para instalar dependencias de Python, Docker y el modelo YOLO de forma estandarizada. |
| Idempotencia | La ejecución de un Playbook siempre lleva el sistema al estado deseado, independientemente de su estado inicial. Si una dependencia ya está instalada, Ansible no intentará instalarla de nuevo. | Fiabilidad: Asegura que la configuración de cada nodo del cluster de IA sea exactamente la misma, sin duplicidades. |
| Integración IaC | Se utiliza comúnmente después de aprovisionar la infraestructura con Terraform para realizar la configuración inicial. | Flujo DevOps: Permite un flujo continuo: Terraform crea la VM → Ansible instala el software y despliega el contenedor Docker. |

---

### c) 🐇 RabbitMQ: Mensajería Asíncrona Robusta (Broker)

RabbitMQ es un broker de mensajes open source basado en el estándar AMQP (Advanced Message Queuing Protocol). Su función principal es desacoplar las aplicaciones, permitiendo que se comuniquen de forma asíncrona.

| Concepto    | Rol en la Arquitectura | Beneficio para SIMA |
|-------------|-------------------------|----------------------|
| Broker | El servidor central que recibe, almacena y envía mensajes. | Fiabilidad: Los mensajes se almacenan hasta que el consumidor los procesa, evitando la pérdida de alertas críticas (detecciones de YOLO) si el servidor de Streamlit está caído. |
| Productor | El componente que envía mensajes a una cola (ej. el Módulo de Detección YOLO). | Desacoplamiento: El módulo YOLO solo necesita saber dónde enviar la alerta, sin preocuparse si el dashboard de Streamlit está escuchando en ese momento. |
| Consumidor | El componente que recibe y procesa mensajes de una cola (ej. el Módulo Streamlit/Base de Datos). | Escalabilidad: Se pueden añadir múltiples consumidores (ej. un servicio que envía emails y otro que actualiza la BD) sin modificar el código del productor (YOLO). |
| Asincronía | La comunicación no requiere una respuesta inmediata. | Eficiencia: El procesamiento de imágenes pesadas de YOLO no bloquea el envío inmediato de la alerta, acelerando el tiempo de respuesta del sistema. |

---

### d) ☁️ Tecnologías OpenStack para la Generación de Nubes Propias

OpenStack es un conjunto de herramientas de software open source para construir y gestionar plataformas de cloud computing para nubes públicas y privadas. Es la alternativa open source a AWS, Azure o Google Cloud, esencial para infraestructuras soberanas o privadas (como podría ser un cluster dedicado de MinCiencias).

| Componente Clave | Función Principal | Analogía en la Nube Pública |
|------------------|-------------------|------------------------------|
| Nova | Proporciona el servicio de Computación. Gestión de Máquinas Virtuales (VMs) y contenedores. | EC2 (AWS), Compute Engine (GCP) |
| Swift / Cinder | Proporcionan servicios de Almacenamiento de Objetos (Swift) y de Bloques (Cinder) para VMs. | S3 (AWS), Persistent Disk (GCP) |
| Neutron | Ofrece el servicio de Redes. Permite a los usuarios crear redes virtuales, routers y direcciones IP. | VPC (AWS), Virtual Network (Azure) |
| Keystone | Proporciona el servicio de Identidad y Acceso. Gestiona usuarios, roles y permisos de los proyectos. | IAM (AWS), Cloud IAM (GCP) |

---

## Relevancia para la Convocatoria de MinCiencias:

Si la infraestructura de la convocatoria no se basa puramente en nubes comerciales, sino en un cluster de cómputo propio (Cloud Privada o Híbrida) dentro de una entidad pública o universidad, es altamente probable que esté gestionada por OpenStack. Conocer OpenStack asegura que los ingenieros puedan aprovisionar recursos de IA (VMs con GPUs para YOLO) y configurar las redes necesarias para la comunicación de RabbitMQ utilizando estándares abiertos.

---

## 🔗 Integración y Orquestación: De IaC al Contenedor

La eficiencia en el despliegue de soluciones de Inteligencia Artificial (IA) en entornos de producción (como el propuesto por la convocatoria) se logra mediante la automatización completa del ciclo de vida de la infraestructura y el software.

La siguiente secuencia describe un flujo continuo donde Terraform, Ansible, y Docker actúan de forma concertada para desplegar y configurar el Sistema Inteligente de Monitoreo Ambiental (SIMA).

### 1. ⚙️ Etapa 1: Aprovisionamiento de la Infraestructura con Terraform (IaC)

El proceso inicia con la definición del hardware y la red necesarios para alojar los módulos de IA.

- Acción de Terraform: Usando archivos .tf escritos en HCL, Terraform se comunica con el proveedor de la nube (ej. OpenStack o la nube elegida por MinCiencias) y ejecuta el comando terraform apply.

- Recursos Creados para SIMA:

- - Máquinas Virtuales (VMs) de Cómputo: Crea dos o más instancias de VM (basadas en Ubuntu), posiblemente con aceleradores gráficos (GPU) para el Módulo de Detección YOLO.

- - Base de Datos y Broker: Aprovisiona instancias dedicadas para la base de datos de alertas y para el servidor de mensajería RabbitMQ.

- - Networking: Configura las subredes, reglas de firewall (puertos 22/SSH, 8501/Streamlit y 5672/RabbitMQ) y Balanceadores de Carga (para distribuir el tráfico a múltiples instancias de Streamlit).

Resultado: Se obtiene una infraestructura de red estable y replicable, con direcciones IP definidas para cada componente (VMs de Ubuntu).

---

### 2. 🗄️ Etapa 2: Configuración y Preparación con Ansible

Una vez que las VMs están levantadas, Ansible toma el control para configurar el sistema operativo y preparar el entorno para la aplicación. Ansible utiliza el inventario de IPs generado automáticamente por Terraform.

- Playbook de Pre-requisitos: Ansible se conecta vía SSH a las VMs de Ubuntu (sin necesidad de agentes) y ejecuta los siguientes playbooks:

- - Instalación de utilidades base y configuración de seguridad.

- - Instalación del runtime de Docker en las VMs de YOLO y Streamlit.

- - Configuración específica del host (ej. montar volúmenes persistentes para los modelos de YOLO y los datos de entrenamiento).

- Playbook de Despliegue de Aplicaciones Secundarias:

- - Garantiza que el broker RabbitMQ esté configurado y corriendo con las colas y usuarios correctos para el envío de alertas.

Resultado: Las máquinas Ubuntu están listas; tienen Docker instalado y el broker de mensajería ya está operativo, esperando los mensajes.

---

### 3. 📦 Etapa 3: Despliegue de la Aplicación con Docker

Ansible, como gestor de configuración, también puede iniciar el despliegue final de la aplicación, aprovechando la portabilidad de los contenedores Docker.

- Rol del Contenedor: Ansible puede ejecutar comandos docker-compose o docker run en las VMs de Ubuntu.

- Despliegue de Módulos SIMA:

- - Despliega el contenedor YOLO/OpenCV (Productor), el cual es un ejecutable autónomo. Este contenedor comienza a recibir imágenes para el análisis y a enviar mensajes de alerta al broker RabbitMQ.

- - Despliega el contenedor Streamlit (Consumidor), el cual se inicializa y se conecta a RabbitMQ para leer las alertas en tiempo real y mostrarlas en el dashboard.

Resultado: El sistema SIMA está completamente operativo y accesible, con todos sus módulos funcionando dentro de contenedores aislados y gestionados.

---

### 4. ✉️ El Rol Desacoplador de RabbitMQ

La integración de RabbitMQ es vital en este pipeline de IA para garantizar la alta disponibilidad y el desacoplamiento de los módulos:

| Flujo de Información | Uso de RabbitMQ | Impacto Operacional |
|----------------------|------------------|----------------------|
| YOLO → Streamlit | El módulo YOLO (Productor) publica un mensaje de "alerta de riesgo" en una cola. | Resiliencia: Si el servidor de Streamlit se reinicia, el mensaje permanece seguro en RabbitMQ y no se pierde, siendo procesado tan pronto como Streamlit se recupere. |
| Escalado | Se pueden añadir nuevas instancias de YOLO para aumentar la capacidad de procesamiento de imágenes. | Simplicidad: Los nuevos productores solo necesitan la dirección del broker, sin afectar a los consumidores (Streamlit). |

Esta cadena de herramientas (Terraform $\rightarrow$ Ansible $\rightarrow$ Docker/RabbitMQ) representa el estándar moderno de DevOps, permitiendo la velocidad, fiabilidad y escalabilidad necesarias para un proyecto de infraestructura de IA de MinCiencias.

---

## 📚 Referencias

La información presentada en esta documentación técnica se fundamenta en los siguientes recursos especializados en Arquitectura de Sistemas, DevOps e Infraestructura como Código (IaC):

### 1. Infraestructura como Código (Terraform)

- HashiCorp. (2024). Terraform Documentation. Recuperado de: https://developer.hashicorp.com/terraform/docs

### 2. Automatización y Gestión de Configuración (Ansible)

- Ansible Documentation. Introduction to Ansible. Recuperado de: https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html

### 3. Mensajería Asíncrona (RabbitMQ)

- Videla, G. (2018). RabbitMQ Essentials: The Advanced Message Queuing Protocol (AMQP) in Practice. Packt Publishing.

### 4. Cloud Computing Open Source (OpenStack)

OpenStack Foundation. OpenStack Documentation: Project Navigator. Recuperado de: https://docs.openstack.org/
