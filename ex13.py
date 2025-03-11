import requests
import pytest

# Данные из списка User-Agent и ожидаемых значений
USER_AGENTS_TEST_DATA = [
    (
    "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Android", "No", "Mobile"),
    (
    "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
    "iOS", "Chrome", "Mobile"),
    (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Unknown", "Unknown", "Googlebot"),
    (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
    "No", "Chrome", "Web"),
    (
    "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "iPhone", "No", "Mobile"),
]


@pytest.mark.parametrize("user_agent, expected_device, expected_browser, expected_platform", USER_AGENTS_TEST_DATA)
def test_user_agent_check(user_agent, expected_device, expected_browser, expected_platform):
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    headers = {"User-Agent": user_agent}

    response = requests.get(url, headers=headers)
    response_json = response.json()
    print(response_json)

    actual_device = response_json.get("device", "Unknow")
    actual_browser = response_json.get("browser", "Unknow")
    actual_platform = response_json.get("platform", "Unknow")

    errors = []
    if actual_device != expected_device:
        errors.append(f"Device mismatch: expected '{expected_device}', got '{actual_device}'")
    if actual_browser != expected_browser:
        errors.append(f"Browser mismatch: expected '{expected_browser}', got '{actual_browser}'")
    if actual_platform != expected_platform:
        errors.append(f"Platform mismatch: expected '{expected_platform}', got '{actual_platform}'")

    assert not errors, f"User-Agent: {user_agent}\n" + "\n".join(errors)
