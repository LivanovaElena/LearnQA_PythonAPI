import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect', allow_redirects=True)
response_quantity = len(response.history)
print(response_quantity)
print(response.history[response_quantity - 1].url)