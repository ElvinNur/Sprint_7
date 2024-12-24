import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

class TestGetOrder:
    @pytest.mark.parametrize("params", [
    {},
    {"courierId": 1},
    {"nearestStation": ["1", "2"]},
    {"limit": 5, "page": 2}])
    def test_get_orders_list(self, params):
        
        response = requests.get(BASE_URL, params=params)
        assert response.status_code == 200, (
            f"Ожидали код ответа 200, а получили {response.status_code}")

        body = response.json()
        assert "orders" in body, (
            f"В теле ответа нет ключа 'orders': {body}")

        orders = body["orders"]
        assert isinstance(orders, list), (
            f"Ожидали, что 'orders' будет списком, а получили {type(orders)}: {orders}")