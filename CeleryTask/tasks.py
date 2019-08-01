from __future__ import absolute_import
from DjangoShop.celery import app  # 在安装celery框架成功后，django新生成的模块

@app.task # 将taskExample转换为一个任务
def taskExample():
    print("send email ok!")

@app.task
def add(x=1,y=2):
    return x+y

