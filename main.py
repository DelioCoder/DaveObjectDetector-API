from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()

# Habilita CORS para que Next.js pueda hacer requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cámbialo a tu dominio en producción
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga tu modelo personalizado (ajusta si lo guardaste en otro lugar)
model = YOLO("yolov8n.pt")

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    # Lee imagen
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Ejecuta la detección
    results = model(img)[0]

    # Procesa resultados
    objects = []
    for box, cls in zip(results.boxes, results.boxes.cls):
        label = model.names[int(cls)]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        objects.append({
            "label": label,
            "bbox": [x1, y1, x2, y2]
        })

    return { "objects": objects }
