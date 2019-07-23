import hashlib

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse

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
    # 前端校验
    result = {"status": "error", "data": ""}
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
    # 后端校验
    result = {"status":"error","data":""}
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
                    result["status"] = "success"
                    result["data"] = "登录成功"
                    return response
                else:
                    result["data"] = "密码错误"
                    response = render(request, "store/login.html", locals())
            else:
                result["data"] = "用户名不存在"
                response = render(request, "store/login.html", locals())
        else:
            result["data"] = "用户名或密码不能为空"
            response = render(request, "store/login.html",locals())
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

# 前端注册功能用户校验
def ajax_regValid(request):
    # ajax前端注册校验
    result = {"status": "error", "data": ""}
    username = request.POST.get("username")
    if username:
        user = Seller.objects.filter(username=username).first() # 数据库查询该用户
        if user:
            result["data"] = "用户名已存在"
        else:
            result["status"] = "success"
            result["data"] = "用户名可以使用"
    else:
        result["data"] = "用户名不能为空"
    return JsonResponse(result)

# 退出功能（删除cookie)
def exit(request):
    response = HttpResponseRedirect("/Store/login/")
    response.delete_cookie("username")
    del request.session["username"]
    return response


def base(request):
    return render(request,"store/base.html")