import pytest
from faker import Faker
from helpers import UserApi

@pytest.fixture
def random_user():
    fake = Faker()
    email = fake.email()
    password = fake.password()
    name = fake.first_name()
    return {"email": email, "password": password, "name": name}

@pytest.fixture
def create_and_delete_user():
    fake = Faker()
    payload = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name()
    }
    
    # Создаем пользователя
    response = UserApi.register_user(payload)
    access_token = response.json().get("accessToken")
    
    yield payload, access_token
    
    # Удаляем пользователя после теста
    if access_token:
        UserApi.delete_user(access_token)
