import pytest
import requests
from config import COURIER_URL
from helpers import _generate_random_string


@pytest.mark.courier
class TestCreateCourier:

    def test_create_courier_success(self, create_and_delete_courier):
        courier_data, courier_id = create_and_delete_courier

        response = requests.post(f"{COURIER_URL}/login", json={
            "login": courier_data["login"],
            "password": courier_data["password"]})
        
        assert response.status_code == 200, (
            f"Не удалось авторизоваться после создания курьера: {response.status_code}")
        
        body = response.json()
        assert body.get("id") == courier_id, "Полученный ID не совпадает с ожидаемым"

    def test_cannot_create_two_identical_couriers(self, create_and_delete_courier):
        courier_data, _ = create_and_delete_courier

        response = requests.post(COURIER_URL, json=courier_data)
        assert response.status_code == 409, (
            f"Повторное создание такого же курьера вернуло {response.status_code}, ожидали 409")
        
        body = response.json()
        assert body.get("message") == "Этот логин уже используется"

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": _generate_random_string(),
            "password": _generate_random_string(),
            "firstName": _generate_random_string()}

        del payload[missing_field]

        response = requests.post(COURIER_URL, json=payload)
        assert response.status_code == 400, (
            f"При отсутствии поля {missing_field} ожидался статус 400, а пришёл {response.status_code}")
        
        body = response.json()
        assert body.get("message") == "Недостаточно данных для создания учетной записи"

    def test_create_courier_with_existing_login(self, create_and_delete_courier):
        courier_data, _ = create_and_delete_courier

        response = requests.post(COURIER_URL, json={
            "login": courier_data["login"],
            "password": _generate_random_string(),
            "firstName": _generate_random_string()})
        
        assert response.status_code == 409, (
            f"При создании курьера с занятым логином ожидали 409, а получили {response.status_code}")
        
        body = response.json()
        assert body.get("message") == "Этот логин уже используется"

