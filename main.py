from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"message": "API is awake!"}
#Modelo
model = YOLO("yolov8n.pt")

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    
    try:

        allowed_types = ["image/jpeg", "image/jpg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Formato de archivo no permitido. Solo jpg, jpeg y png.")

        contents = await file.read()
        npimg = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return {"error": "No se pudo procesar la imagen"}

        # Detección
        results = model(img)[0]

        objects = []
        for box, cls in zip(results.boxes, results.boxes.cls):
            label = model.names[int(cls)]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            objects.append({
                "label": label,
                "bbox": [x1, y1, x2, y2]
            })

        return {"objects": objects}

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

    finally:
        del file
        del contents
        if 'npimg' in locals():
            del npimg
        if 'img' in locals():
            del img
        if 'results' in locals():
            del results
