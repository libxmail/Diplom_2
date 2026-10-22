import requests
from data import StellarBurgersUrls

class UserApi:
    @staticmethod
    def register_user(payload):
        return requests.post(StellarBurgersUrls.URL_REGISTER, json=payload, timeout=10)

    @staticmethod
    def login_user(payload):
        return requests.post(StellarBurgersUrls.URL_LOGIN, json=payload, timeout=10)

    @staticmethod
    def delete_user(access_token):
        headers = {"Authorization": access_token}
        return requests.delete(StellarBurgersUrls.URL_USER, headers=headers, timeout=10)

class OrderApi:
    @staticmethod
    def create_order(payload, access_token=None):
        headers = {"Authorization": access_token} if access_token else {}
        return requests.post(StellarBurgersUrls.URL_ORDERS, json=payload, headers=headers, timeout=10)

    @staticmethod
    def get_ingredients():
        return requests.get(StellarBurgersUrls.URL_INGREDIENTS, timeout=10)