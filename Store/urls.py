from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    re_path(r'^$',index),
    path('ajax/',ajax_regValid),
    path('exit/', exit),
    path('store_register/', store_register),
    path('add_good/', add_goods),
    path('list_goods_type/', goods_type_list),
    path('delete_goods_type/', delete_goods_type),

]

urlpatterns += [
    re_path(r'^goods/(?P<goods_id>\d+)', goods),
    re_path(r'update_goods/(?P<goods_id>\d+)', update_goods),
    re_path(r'goods_list/(?P<state>\w+)/', list_goods),
    re_path(r'set_goods/(?P<state>\w+)/', set_goods),
]