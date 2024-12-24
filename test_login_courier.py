import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def _generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class TestCourierLogin:
    
    def test_courier_can_login(self):
        login = _generate_random_string()
        password = _generate_random_string()
        first_name = _generate_random_string()
        create_response = requests.post(f"{BASE_URL}/courier", json={
            "login": login,
            "password": password,
            "firstName": first_name})
        assert create_response.status_code == 201, "Не удалось создать курьера перед логином"

        login_response = requests.post(f"{BASE_URL}/courier/login", json={
            "login": login,
            "password": password})
        
        assert login_response.status_code == 200, (
            f"Курьер не смог авторизоваться, статус {login_response.status_code}")
        
        body = login_response.json()
        assert "id" in body, f"В ответе при успешном логине нет поля 'id': {body}"


    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field):

        data = {"login": _generate_random_string(),
            "password": _generate_random_string()}
        
        del data[missing_field]

        response = requests.post(f"{BASE_URL}/courier/login", json=data)
        
        assert response.status_code == 400, (
            f"Ожидали 400 при отсутствии поля {missing_field}, получили {response.status_code}")

        body = response.json()
        assert body.get("message") == "Недостаточно данных для входа"

    def test_login_incorrect_credentials(self):
        wrong_login = _generate_random_string()
        wrong_password = _generate_random_string()

        response = requests.post(f"{BASE_URL}/courier/login", json={
            "login": wrong_login,
            "password": wrong_password})

        assert response.status_code == 404, (
            f"При неправильных логине/пароле ожидался статус 404, а получили {response.status_code}")
        body = response.json()
        assert body.get("message") == "Учетная запись не найдена"


    def test_success_response_contains_id(self):
        login = _generate_random_string()
        password = _generate_random_string()
        first_name = _generate_random_string()
        create_resp = requests.post(f"{BASE_URL}/courier", json={
            "login": login,
            "password": password,
            "firstName": first_name})
        assert create_resp.status_code == 201, "Создание курьера не удалось"

        login_resp = requests.post(f"{BASE_URL}/courier/login", json={
            "login": login,
            "password": password})
        body = login_resp.json()
        assert "id" in body, f"Ожидали поле 'id', а получили {body}"
        assert body["id"], f"id пустой или None: {body['id']}"