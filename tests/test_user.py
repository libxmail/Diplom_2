import allure
import pytest
from helpers import UserApi
from data import StellarBurgersUrls

class TestUserRegistration:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, random_user):
        response = UserApi.register_user(random_user)
        assert response.status_code == 200
        assert response.json()["success"] is True
        
        access_token = response.json().get("accessToken")
        if access_token:
            UserApi.delete_user(access_token)

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_and_delete_user):
        payload, _ = create_and_delete_user
        
        response = UserApi.register_user(payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя с пропуском обязательного поля")
    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, random_user, field_to_remove):
        incomplete_payload = random_user.copy()
        del incomplete_payload[field_to_remove]
        
        response = UserApi.register_user(incomplete_payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == "Email, password and name are required fields"


class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user(self, create_and_delete_user):
        payload, access_token = create_and_delete_user
        login_data = {
            "email": payload["email"],
            "password": payload["password"]
        }
        
        response = UserApi.login_user(login_data)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином или паролем")
    def test_login_invalid_credentials(self, create_and_delete_user):
        payload, _ = create_and_delete_user
        invalid_login_data = {
            "email": payload["email"],
            "password": "wrong_password"
        }
        
        response = UserApi.login_user(invalid_login_data)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "email or password are incorrect"
        