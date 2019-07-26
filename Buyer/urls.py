from django.urls import path
from Buyer.views import *
# v2.6 新建buyer app 的独立url
urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('index/', index),
    path('goods_list/', goods_list),
]

urlpatterns += [
    path('base/', base),

]