import requests


def test_homework_header():
    url = "https://playground.learnqa.ru/api/homework_header"

    response = requests.get(url)
    headers = response.headers

    assert headers, "No headers found in the response"

    for key, value in headers.items():
        print(f"Header: {key} -> {value}")

    # Ожидаемые заголовки (полученные через print)
    expected_headers = {
        "Content-Type": "application/json",
        "Content-Length": "15",
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=10",
        "Server": "Apache",
        "x-secret-homework-header": "Some secret value"
    }

    for key, expected_value in expected_headers.items():
        assert key in headers, f"Expected header '{key}' not found"
        assert headers[key] == expected_value, \
            f"Unexpected value for header '{key}': {headers[key]}"

