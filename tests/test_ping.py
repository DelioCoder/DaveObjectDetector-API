from fastapi.testclient import TestClient  # Importa el cliente de pruebas para simular peticiones HTTP
from main import app                       # Importa la instancia FastAPI definida en main.py

client = TestClient(app)                   # Crea un cliente de pruebas usando la app FastAPI

def test_ping():                          # Define la función de prueba para el endpoint /ping
    response = client.get("/ping")        # Envía una petición GET al endpoint /ping
    assert response.status_code == 200   # Verifica que el código HTTP de la respuesta sea 200 (OK)
    assert response.json() == {"message": "API is awake!"}  # Verifica que la respuesta JSON sea la esperada
