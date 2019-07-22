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
    """
    登录功能：进入登录页面是下发cookie，验证是正常方式请求登录
    登录成功再次下发一个cookie，验证用户
    """
    # 进入登录页面下发来源合法的cookie
    response = render(request,"store/login.html")
    response.set_cookie("login_from","legitimate")
    # 判断用户请求的方式
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password: # 用户和密码都存在
            seller = Seller.objects.filter(username=username).first() # 数据库查询该用户
            if seller:
                # 将前端获取到的密码加密，同数据库进行验证
                web_password = setPassword(password)
                # 校验登录页面的cookie
                cookies = request.COOKIES.get("login_from")
                if web_password == seller.password and cookies == "legitimate":
                    # 登录成功，则跳转到首页并下发cookie和session
                    response = HttpResponseRedirect('/Store/index/')
                    response.set_cookie("username",seller.username)
                    request.session["username"] = seller.username
                    return response
    return response

# 用户登录校验装饰器
def loginValid(fun):
    def inner(request,*args,**kwargs):
        # 获取成功登录后的cookie和session
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        # 如果cookie和session都存在并且值都相同
        if c_user and s_user and c_user == s_user:
            # 通过c_user查询数据库
            seller = Seller.objects.filter(username=c_user).first()
            # 如果有这个用户，则返回函数，这里只index
            if seller:
                return fun(request,*args,**kwargs)
        # 否则重定向到登录页面
        return HttpResponseRedirect("/Store/login/")
    return inner

# 首页
@loginValid
def index(request):
    return render(request,"store/index.html",locals())