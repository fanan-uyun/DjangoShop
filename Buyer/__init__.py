import os
from django.apps import AppConfig


default_app_config = 'Buyer.BuyerConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class BuyerConfig(AppConfig):
    name = 'Buyer'
    verbose_name = "买家"