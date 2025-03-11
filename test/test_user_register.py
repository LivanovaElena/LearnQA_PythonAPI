import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import string


BASE_URL = "https://playground.learnqa.ru/api/user/"


class TestUserRegister(BaseCase):

    def test_create_user_invalid_email(self):
        """Создание пользователя с некорректным email - без символа @"""
        data = {
            "username": "testuser",
            "firstName": "Test",
            "lastName": "User",
            "email": "invalidemail.com",  # некорректный email
            "password": "1234"
        }
        response = requests.post(BASE_URL, data=data)
        assert response.status_code == 400, "Ожидался код 400 при некорректном email"
        assert "Invalid email format" in response.text, "Ожидалось сообщение о неверном формате email"

    @pytest.mark.parametrize("missing_field", [
        "username", "firstName", "lastName", "email", "password"
    ])
    def test_create_user_missing_field(self, missing_field):
        """Создание пользователя без одного из обязательных полей"""
        data = {
            "username": "testuser",
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "password": "1234"
        }
        data.pop(missing_field)  # Удаляем одно поле

        response = requests.post(BASE_URL, data=data)
        assert response.status_code == 400, f"Ожидался код 400 при отсутствии поля {missing_field}"
        assert f"The following required params are missed: {missing_field}" in response.text, f"Ожидалось сообщение о нехватке {missing_field}"

    def test_create_user_short_name(self):
        """Создание пользователя с очень коротким именем в один символ"""
        data = {
            "username": "a",
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "password": "1234"
        }
        response = requests.post(BASE_URL, data=data)
        assert response.status_code == 400, "Ожидался код 400 при слишком коротком имени"
        assert "The value of 'username' field is too short" in response.text, "Ожидалось сообщение о слишком коротком имени"

    def test_create_user_long_name(self):
        """Создание пользователя с очень длинным именем (более 250 символов)"""
        long_username = "a" * 251
        data = {
            "username": long_username,
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "password": "1234"
        }
        response = requests.post(BASE_URL, data=data)
        assert response.status_code == 400, "Ожидался код 400 при слишком длинном имени"
        assert "The value of 'username' field is too long" in response.text, "Ожидалось сообщение о слишком длинном имени"

    def test_create_user_with_existing_email(self):
        """Создание пользователя с уже существующим email"""
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post(BASE_URL, data=data)
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert "Users with email" in response.text and email in response.text, f"Unexpected response content {response.text}"
