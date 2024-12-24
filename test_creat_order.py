import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

def _random_string(length=5):

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

class TestCreateOrder:
    @pytest.mark.parametrize("color", [["BLACK"],   
    ["GREY"],
    ["BLACK", "GREY"],
    []])
    def test_create_order_with_various_colors(self, color):

        payload = {
            "firstName": _random_string(),
            "lastName": _random_string(),
            "address": _random_string(10),
            "metroStation": "Nekrasovka",
            "phone": "+7 900 000 00 00",
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Test order",
            "color": color}

        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 201, (
            f"Ожидали статус-код 201 при создании заказа, а получили {response.status_code}")

        body = response.json()
        assert "track" in body, (
            f"В ответе отсутствует ключ 'track': {body}")