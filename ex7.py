import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ["GET", "POST", "PUT", "DELETE"]

# 1. http-запрос любого типа без параметра method
response_no_param = requests.get(url)
print("1. Request: GET without method param")
print("Response code:", response_no_param.status_code)
print("Response text:", response_no_param.text)
print("----------------------------------------")

# 2. http-запрос не из списка. Например, HEAD
response_head = requests.head(url, params={"method": "HEAD"})
print("2. Request: HEAD with method param 'HEAD'")
print("Response code:", response_head.status_code)
print("Response text:", response_head.text)
print("----------------------------------------")

# 3. Запрос с правильным значением method
for method in methods:
    if method == "GET":
        response = requests.get(url, params={"method": method})
    else:
        response = requests.request(method, url, data={"method": method})
    print(f"3. Request: {method} with correct method param '{method}'")
    print("Response code:", response.status_code)
    print("Response text:", response.text)
    print("----------------------------------------")

# 4. Проверка всех возможных сочетаний реального типа запроса и параметра method
for real_method in methods:
    for param_method in methods:
        if real_method == "GET":
            response = requests.get(url, params={"method": param_method})
        else:
            response = requests.request(real_method, url, data={"method": param_method})

        print(f"4. Request: {real_method} with param method '{param_method}'")
        print("Response code:", response.status_code)
        print("Response text:", response.text)

        if real_method != param_method and "success" in response.text:
            print("⚠️ Unexpected success! Real method:", real_method, "Param method:", param_method)
        elif real_method == param_method and "success" not in response.text:
            print("⚠️ Expected success but got something else! Real method:", real_method, "Param method:",
                  param_method)

        print("----------------------------------------")