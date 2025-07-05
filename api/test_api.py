import pytest
import json
from app import app
from model import Session, Paciente

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        cleanup_test_patients()
        yield client
        cleanup_test_patients()

@pytest.fixture
def sample_patient_data():
    return {
        "name": "Paciente de Teste",
        "age": 55.0,
        "cp": 4.0,
        "thalach": 140.0,
        "exang": 1.0,
        "oldpeak": 3.0,
        "ca": 1.0,
        "thal": 7.0
    }

def add_sample_patient_to_db(data):
    session = Session()
    paciente_teste = Paciente(
        name=data["name"], age=data["age"], cp=data["cp"], thalach=data["thalach"],
        exang=data["exang"], oldpeak=data["oldpeak"], ca=data["ca"], thal=data["thal"],
        outcome=1
    )
    session.add(paciente_teste)
    session.commit()
    session.close()

def test_add_patient_prediction(client, sample_patient_data):
    response = client.post('/paciente', json=sample_patient_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == sample_patient_data['name']
    assert 'outcome' in data

def test_add_duplicate_patient(client, sample_patient_data):
    add_sample_patient_to_db(sample_patient_data)
    response = client.post('/paciente', json=sample_patient_data)
    assert response.status_code == 409

def test_get_nonexistent_patient(client):
    response = client.get('/paciente?name=Fantasma')
    assert response.status_code == 404

def test_delete_patient(client, sample_patient_data):
    add_sample_patient_to_db(sample_patient_data)
    response = client.delete(f'/paciente?name={sample_patient_data["name"]}')
    assert response.status_code == 200

def cleanup_test_patients():
    session = Session()
    session.query(Paciente).filter(Paciente.name == "Paciente de Teste").delete()
    session.commit()
    session.close()