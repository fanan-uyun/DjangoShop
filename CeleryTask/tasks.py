from __future__ import absolute_import
import requests
import json
from DjangoShop.celery import app  # 在安装celery框架成功后，django新生成的模块

@app.task # 将taskExample转换为一个任务
def taskExample():
    print("send email ok!")

@app.task
def add(x=1,y=2):
    return x+y

@app.task
def DingTalk():
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

    response = requests.post(url, headers=headers, data=sendData)

    content = response.json()

    print(content)
