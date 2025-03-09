import requests


def test_homework_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"

    response = requests.get(url)
    cookies = response.cookies

    assert cookies, "No cookies in response"

    for key, value in cookies.items():
        print(f"Cookie name: {key}, Cookie value: {value}")

    # Ожидаемая кука (полученная через print)
    expected_cookie_name = "HomeWork"
    expected_cookie_value = "hw_value"

    assert expected_cookie_name in cookies, f"Expected cookie '{expected_cookie_name}' not found"

    assert cookies[expected_cookie_name] == expected_cookie_value, \
        f"Unexpected value for cookie '{expected_cookie_name}': {cookies[expected_cookie_name]}"

