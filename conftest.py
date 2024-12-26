import pytest
import requests
from config import COURIER_URL
from helpers import _generate_random_string

@pytest.fixture
def create_and_delete_courier():
    
    courier_data = {
        "login": _generate_random_string(),
        "password": _generate_random_string(),
        "firstName": _generate_random_string()}

    response = requests.post(COURIER_URL, json=courier_data)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.status_code}"
    
    login_response = requests.post(f"{COURIER_URL}/login", json={
        "login": courier_data["login"],
        "password": courier_data["password"]})
    
    assert login_response.status_code == 200, (
        f"Не удалось авторизоваться: {login_response.status_code}, {login_response.text}")
    
    login_body = login_response.json()
    courier_id = login_body.get("id")
    assert courier_id, "Не удалось получить ID курьера при авторизации"

    yield courier_data, courier_id

    delete_response = requests.delete(f"{COURIER_URL}/{courier_id}")
    assert delete_response.status_code == 200, (
        f"Не удалось удалить курьера: {delete_response.status_code}, {delete_response.text}")