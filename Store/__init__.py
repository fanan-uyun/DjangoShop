import os
from django.apps import AppConfig


default_app_config = 'Store.StoreConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class StoreConfig(AppConfig):
    name = 'Store'
    verbose_name = "商家"