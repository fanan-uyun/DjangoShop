import hashlib

from django.shortcuts import render
from django.http import HttpResponseRedirect

from Store.models import *

# Create your views here.
# 密码加密功能
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

# 注册功能
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = setPassword(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect("/Store/login/")
    return render(request,"store/register.html")


# 登录功能
def login(request):
    return render(request,"store/login.html")