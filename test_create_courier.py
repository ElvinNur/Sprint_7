import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

def _generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@pytest.mark.courier
class TestCreateCourier:

    def test_create_courier_success(self):
        payload = {"login": _generate_random_string(),
            "password": _generate_random_string(),
            "firstName": _generate_random_string()}
        
        response = requests.post(BASE_URL, json=payload)

        assert response.status_code == 201, (f"Ожидался статус 201, но пришёл {response.status_code}")
        
        body = response.json()
        assert body.get("ok") is True, f"Ожидали {{'ok': true}}, а получили {body}"

    def test_cannot_create_two_identical_couriers(self):
        courier_data = {"login": _generate_random_string(),
            "password": _generate_random_string(),
            "firstName": _generate_random_string()}

        response1 = requests.post(BASE_URL, json=courier_data)
        assert response1.status_code == 201, (f"Первое создание курьера вернуло {response1.status_code}, ожидали 201")

        response2 = requests.post(BASE_URL, json=courier_data)
        assert response2.status_code == 409, (
            f"Повторное создание такого же курьера вернуло {response2.status_code}, ожидали 409")


    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):

        payload = {
            "login": _generate_random_string(),
            "password": _generate_random_string(),
            "firstName": _generate_random_string()}
        
        del payload[missing_field]

        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 400, (
            f"При отсутствии поля {missing_field} ожидался статус 400, а пришёл {response.status_code}")


    def test_create_courier_with_existing_login(self):

        login = _generate_random_string()
        password = _generate_random_string()
        first_name = _generate_random_string()

        response1 = requests.post(BASE_URL, json={
            "login": login,
            "password": password,
            "firstName": first_name
        })
        assert response1.status_code == 201, (
            f"При создании курьера вернулся статус {response1.status_code}, ожидали 201")

        response2 = requests.post(BASE_URL, json={
            "login": login,
            "password": _generate_random_string(), 
            "firstName": _generate_random_string()})
        
        assert response2.status_code == 409, (
            f"При создании курьера с занятым логином ожидали 409, а получили {response2.status_code}") 

