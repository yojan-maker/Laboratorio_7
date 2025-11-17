## 🖼️ 1. Análisis de Sentimientos por Imágenes con MediaPipe, Hilos, Mutex y Semáforos

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

## 2) 📘 Desarrollo de un ETL partiendo de una base de datos

---

### 🎯 Objetivo del Punto 2

El objetivo es desarrollar un pipeline ETL funcional, entrenar un modelo simple y desplegar un dashboard interactivo en Streamlit, integrando diferentes conceptos del curso.

Específicamente, se busca:

* Desarrollar un **ETL completo** a partir de la base de datos proporcionada en clase (o datos sintéticos en caso de ausencia).
* Aplicar **transformaciones**, generar un dataset procesado.
* Construir un **dashboard con Streamlit** que visualice la información obtenida y los resultados del modelo.

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

1️⃣ Crear entorno virtual
