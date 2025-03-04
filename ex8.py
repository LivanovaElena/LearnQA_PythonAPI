import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1. Создание задачи
response = requests.get(url)
data = response.json()
seconds = data["seconds"]
token = data["token"]
print(f"Task created. Wait time: {seconds} seconds, Token: {token}")

# 2. Запрос до завершения задачи
response_before_completion = requests.get(url, params={"token": token})
data_before_completion = response_before_completion.json()
print("Before completion:", data_before_completion)
assert data_before_completion["status"] == "Job is NOT ready", "Unexpected status before completion"

# 3. Ждем нужное количество секунд
print(f"Waiting for {seconds} seconds...")
time.sleep(seconds)

# 4. Запрос после завершения задачи
response_after_completion = requests.get(url, params={"token": token})
data_after_completion = response_after_completion.json()
print("After completion:", data_after_completion)
assert data_after_completion["status"] == "Job is ready", "Unexpected status after completion"
assert "result" in data_after_completion, "Result field is missing after completion"
