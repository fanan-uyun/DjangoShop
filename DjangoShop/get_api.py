import requests

url = "http://127.0.0.1:8000/APIgoods/"

response = requests.get(url)

json_content = response.json()

for goods in json_content:
    print(goods)