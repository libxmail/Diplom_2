import allure
import requests
from faker import Faker
from data import StellarBurgersUrls


def generate_user_data():
    fake = Faker()
    return {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name()
    }


class UserApi:

    @staticmethod
    @allure.step("Регистрация пользователя")
    def register_user(payload):
        return requests.post(
            StellarBurgersUrls.URL_REGISTER,
            json=payload,
            timeout=10
        )

    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(payload):
        return requests.post(
            StellarBurgersUrls.URL_LOGIN,
            json=payload,
            timeout=10
        )

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(access_token):
        headers = {"Authorization": access_token}
        return requests.delete(
            StellarBurgersUrls.URL_USER,
            headers=headers,
            timeout=10
        )


class OrderApi:

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(payload, access_token=None):
        headers = {"Authorization": access_token} if access_token else {}
        return requests.post(
            StellarBurgersUrls.URL_ORDERS,
            json=payload,
            headers=headers,
            timeout=10
        )

    @staticmethod
    @allure.step("Получение списка ингредиентов")
    def get_ingredients():
        return requests.get(
            StellarBurgersUrls.URL_INGREDIENTS,
            timeout=10
        )
