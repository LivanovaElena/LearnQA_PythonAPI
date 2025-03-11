import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

BASE_URL = "https://playground.learnqa.ru/api/"


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_data_auth_as_another_user(self):
        """Авторизованный запрос на данные другого пользователя должен вернуть только username"""
        # Регистрация и авторизация первого пользователя
        register_data_1 = {
            "username": "user1",
            "firstName": "User",
            "lastName": "One",
            "email": "user1@example.com",
            "password": "1234"
        }
        response1 = requests.post(f"{BASE_URL}user/", data=register_data_1)
        assert response1.status_code == 200, "Не удалось зарегистрировать первого пользователя"
        user_id_1 = response1.json()["id"]

        login_data_1 = {
            "email": register_data_1["email"],
            "password": register_data_1["password"]
        }
        login_response_1 = requests.post(f"{BASE_URL}user/login", data=login_data_1)
        assert login_response_1.status_code == 200, "Не удалось авторизоваться первым пользователем"
        auth_token_1 = login_response_1.cookies.get("auth_sid")

        # Регистрация второго пользователя
        register_data_2 = {
            "username": "user2",
            "firstName": "User",
            "lastName": "Two",
            "email": "user2@example.com",
            "password": "1234"
        }
        response2 = requests.post(f"{BASE_URL}user/", data=register_data_2)
        assert response2.status_code == 200, "Не удалось зарегистрировать второго пользователя"
        user_id_2 = response2.json()["id"]

        # Запрос данных второго пользователя под авторизацией первого
        response_get = requests.get(f"{BASE_URL}user/{user_id_2}", cookies={"auth_sid": auth_token_1})
        assert response_get.status_code == 200, "Ошибка при получении данных другого пользователя"

        response_data = response_get.json()
        expected_fields = ["username"]

        assert list(
            response_data.keys()) == expected_fields, f"Ожидались только {expected_fields}, но получили \{response_data.keys()}"
