import allure
import pytest
from helpers import OrderApi, UserApi
from data import StellarBurgersUrls

class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, create_and_delete_user):
        payload, access_token = create_and_delete_user
        
        ingredients_response = OrderApi.get_ingredients()
        ingredient_id = ingredients_response.json()["data"][0]["_id"]
        
        order_payload = {"ingredients": [ingredient_id]}
        response = OrderApi.create_order(order_payload, access_token)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_unauthorized_with_ingredients(self):
        ingredients_response = OrderApi.get_ingredients()
        ingredient_id = ingredients_response.json()["data"][0]["_id"]
        
        order_payload = {"ingredients": [ingredient_id]}
        response = OrderApi.create_order(order_payload)
        
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_and_delete_user):
        _, access_token = create_and_delete_user
        
        order_payload = {"ingredients": []}
        response = OrderApi.create_order(order_payload, access_token)
        
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self, create_and_delete_user):
        _, access_token = create_and_delete_user
        
        order_payload = {"ingredients": ["invalid_hash_12345"]}
        response = OrderApi.create_order(order_payload, access_token)
        
        assert response.status_code == 500
