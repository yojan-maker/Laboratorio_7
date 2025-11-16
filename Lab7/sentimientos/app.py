  GNU nano 7.2                                                                                                                                                                                         app.py                                                                                                                                                                                                   
import threading
import cv2
import mediapipe as mp
import time

# -----------------------------
#   CONFIGURACIÓN MEDIAPIPE
# -----------------------------
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# -----------------------------
#   SEMÁFORO Y MUTEX
# -----------------------------
mutex = threading.Lock()
semaforo = threading.Semaphore(2)    # solo 2 hilos pueden ejecutar mediapipe al mismo tiempo

resultados = []  # lista compartida donde guardarán el resultado


# -----------------------------
#   FUNCIÓN PARA DETECTAR EMOCIÓN
# -----------------------------
def detectar_sentimiento(imagen_path, nombre_imagen):
    with semaforo:   # máximo 2 hilos simultáneamente
        print(f"[HILO] Procesando: {nombre_imagen}")

        imagen = cv2.imread(imagen_path)
        if imagen is None:
            with mutex:
                resultados.append((nombre_imagen, "ERROR: Imagen no encontrada"))
            return

        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.6) as face_detection:

            resultado = face_detection.process(imagen_rgb)

            if not resultado.detections:
                sentimiento = "SIN ROSTRO DETECTADO"
            else:
                # Aquí puedes poner lógica avanzada, por ahora usamos detección simple
                sentimiento = "ROSTRO DETECTADO"

        # Guardar en resultados protegidos con mutex
        with mutex:
            resultados.append((nombre_imagen, sentimiento))

        print(f"[HILO] Terminado: {nombre_imagen}")


# -----------------------------
#   IMÁGENES A PROCESAR
# -----------------------------
imagenes = [
    ("imagenes/feliz.jpg", "Feliz"),
    ("imagenes/enojado.jpg", "Enojado"),
    ("imagenes/triste.jpg", "Triste")
]

hilos = []

# -----------------------------
#   CREAR Y LANZAR HILOS
# -----------------------------
for path, nombre in imagenes:
    hilo = threading.Thread(target=detectar_sentimiento, args=(path, nombre))
    hilo.start()
    hilos.append(hilo)

# Esperar a que todos terminen
for h in hilos:
    h.join()

# -----------------------------
#   MOSTRAR RESULTADOS
# -----------------------------
print("\n=========== RESULTADOS FINALES ===========")
for nombre, r in resultados:
    print(f"{nombre}: {r}")
print("==========================================")
