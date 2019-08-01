from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings



# 设置celery执行的环境变量，执行django项目的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE","CeleryTask.settings")

# 创建celery应用
app = Celery('celely_task')  # celery应用的名称
app.config_from_object('django.conf:settings')  # 加载的配置文件


# 如果在工程的应用中创建了tasks.py模块，那么Celery应用就会自动去检索创建的任务。比如你添加了一个任#务，在django中会实时地检索出来。
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)