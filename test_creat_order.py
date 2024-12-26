import pytest
import requests
from config import ORDER_URL
from helpers import _generate_random_string


class TestCreateOrder:
    @pytest.mark.parametrize("color", [["BLACK"],   
    ["GREY"],
    ["BLACK", "GREY"],
    []])
    def test_create_order_with_various_colors(self, color):

        payload = {
            "firstName": _generate_random_string(),
            "lastName": _generate_random_string(),
            "address": _generate_random_string(),
            "metroStation": "Nekrasovka",
            "phone": "+7 900 000 00 00",
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Test order",
            "color": color}

        response = requests.post(ORDER_URL, json=payload)
        assert response.status_code == 201, (
            f"Ожидали статус-код 201 при создании заказа, а получили {response.status_code}")

        body = response.json()
        assert "track" in body, (
            f"В ответе отсутствует ключ 'track': {body}")