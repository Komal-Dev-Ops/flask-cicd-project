import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask CI/CD Demo' in response.data

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'

def test_app_info(client):
    response = client.get('/api/info')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['app_name'] == 'Flask CI/CD Demo'
    assert json_data['version'] == '1.0.0'