## 🖼️ 3. Análisis de Sentimientos por Imágenes con MediaPipe, Hilos, Mutex y Semáforos

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
