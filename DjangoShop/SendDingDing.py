#coding:utf-8
import requests
import json

url = "https://oapi.dingtalk.com/robot/send?access_token=3854f74dd13b9cc7ae451c13efdbd0dff0749bf822d792f53b0088f44ad7b37c"

headers = {
    "Content-Type": "application/json",
    "Chartset": "utf-8"
}

requests_data = {
    "msgtype": "text",
    "text": {
        "content": "睡醒了吧，熊大。你亲爱的Mom正在路上了，快点起来了！"
    },
    "at": {
        "atMobiles": [
        ],
        "isAtAll": True
    }
}

sendData = json.dumps(requests_data)

response = requests.post(url,headers=headers,data=sendData)

content = response.json()

print(content)