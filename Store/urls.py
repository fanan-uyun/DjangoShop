from django.urls import path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
]