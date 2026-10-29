import pytest
from helpers import UserApi, generate_user_data


@pytest.fixture
def random_user():
    return generate_user_data()


@pytest.fixture
def create_and_delete_user():
    payload = generate_user_data()
    response = UserApi.register_user(payload)
    access_token = response.json().get("accessToken")

    yield payload, access_token

    if access_token:
        UserApi.delete_user(access_token)


@pytest.fixture
def registered_user():
    payload = generate_user_data()
    response = UserApi.register_user(payload)
    access_token = response.json().get("accessToken")

    yield response

    if access_token:
        UserApi.delete_user(access_token)
