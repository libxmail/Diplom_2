import allure
import pytest
from helpers import UserApi


class TestUserRegistration:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, registered_user):
        assert (
            registered_user.status_code,
            registered_user.json()["success"]
        ) == (200, True)

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_and_delete_user):
        payload, _ = create_and_delete_user

        response = UserApi.register_user(payload)

        assert (
            response.status_code,
            response.json()["success"],
            response.json()["message"]
        ) == (403, False, "User already exists")

    @allure.title("Создание пользователя с пропуском обязательного поля")
    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, random_user, field_to_remove):
        incomplete_payload = random_user.copy()
        del incomplete_payload[field_to_remove]

        response = UserApi.register_user(incomplete_payload)

        assert (
            response.status_code,
            response.json()["success"],
            response.json()["message"]
        ) == (
            403,
            False,
            "Email, password and name are required fields"
        )


class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user(self, create_and_delete_user):
        payload, _ = create_and_delete_user
        login_data = {
            "email": payload["email"],
            "password": payload["password"]
        }

        response = UserApi.login_user(login_data)

        assert (
            response.status_code,
            response.json()["success"],
            "accessToken" in response.json()
        ) == (200, True, True)

    @allure.title("Вход с неверным паролем")
    def test_login_invalid_password(self, create_and_delete_user):
        payload, _ = create_and_delete_user
        login_data = {
            "email": payload["email"],
            "password": "wrong_password"
        }

        response = UserApi.login_user(login_data)

        assert (
            response.status_code,
            response.json()["success"],
            response.json()["message"]
        ) == (
            401,
            False,
            "email or password are incorrect"
        )

    @allure.title("Вход с неверным логином")
    def test_login_invalid_email(self, create_and_delete_user):
        payload, _ = create_and_delete_user
        login_data = {
            "email": "nonexistent_user_123456@example.com",
            "password": payload["password"]
        }

        response = UserApi.login_user(login_data)

        assert (
            response.status_code,
            response.json()["success"],
            response.json()["message"]
        ) == (
            401,
            False,
            "email or password are incorrect"
        )
