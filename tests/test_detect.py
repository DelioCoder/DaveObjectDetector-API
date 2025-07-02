from pathlib import Path                 # Importa Path para manejar rutas de archivos de forma portable
from fastapi.testclient import TestClient  # Importa cliente de pruebas para simular peticiones HTTP
from main import app                     # Importa la instancia FastAPI desde main.py

client = TestClient(app)                 # Crea un cliente de pruebas usando la app FastAPI

def test_detect_with_file():             # Define la función de prueba para el endpoint /detect
    # Construye la ruta al archivo de imagen de prueba relativa a este archivo
    image_path = Path(__file__).parent / "assets" / "test_image.jpeg"
    
    # Abre la imagen en modo lectura binaria
    with open(image_path, "rb") as image_file:
        # Prepara el diccionario 'files' para enviar archivo multipart/form-data
        # Clave 'file' es el nombre esperado en el endpoint, valor es tupla (nombre, contenido, tipo MIME)
        files = {"file": ("test_image.jpeg", image_file, "image/jpeg")}
        
        # Envía petición POST al endpoint /detect con el archivo adjunto
        response = client.post("/detect", files=files)
    
    # Verifica que el código de respuesta HTTP sea 200 OK
    assert response.status_code == 200
    
    # Parsea la respuesta JSON a un diccionario Python
    data = response.json()
    
    # Verifica que la respuesta contenga la clave "objects"
    assert "objects" in data
    
    # Verifica que el valor de "objects" sea una lista
    assert isinstance(data["objects"], list)