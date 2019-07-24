from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    re_path(r'^$',index),
    path('ajax/',ajax_regValid),
    path('exit/', exit),
]

urlpatterns += [
    path('store_register/', store_register),
    path('add_good/', add_goods),
    path('goods_list/', list_goods),
    re_path(r'goods/(?P<goods_id>\d+)', goods)
]