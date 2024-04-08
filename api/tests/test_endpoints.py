import pytest
from fastapi.testclient import TestClient
from ..main import app  # Assurez-vous d'importer votre instance FastAPI depuis votre application

# Créez un client de test pour votre application FastAPI
client = TestClient(app)

# Définissez des tests pour vos endpoints
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API réalisé par KRA FABRICE!"}

def test_predict():
    # Exemple de test pour l'endpoint /predict
    response = client.post("/predict", json={"step": 1, "start_date": "2022-01-01 00:00:00", "end_date": "2022-01-02 00:00:00"})
    assert response.status_code == 200
    assert "predictions" in response.json()

def test_predictions():
    # Exemple de test pour l'endpoint /predictions
    response = client.get("/predictions")
    assert response.status_code == 200
    assert "predictions" in response.json()

def test_predictionsFabio():
    # Exemple de test pour l'endpoint /predictionsFabio
    response = client.get("/predictionsFabio")
    assert response.status_code == 200
    assert "predictions_db" in response.json()
    assert "predictions_csv" in response.json()

# Ajoutez d'autres tests pour vos endpoints

