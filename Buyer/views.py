from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Store.views import setPassword
from Buyer.models import *
from Store.models import *


# Create your views here.
# v2.6 前台用户注册
def register(request):
    if request.method == "POST":
        # 获取前端post请求的数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        # 实例化一个前台用户
        buyer = Buyer()
        # 保存数据
        buyer.username = username
        buyer.password = setPassword(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect('/Buyer/login/')
    return render(request,"buyer/register.html")

# v2.6 前台用户登录
def login(request):
    if request.method == "POST":
        # 获取前端登录页面文本框数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # 判断用户名密码是否存在
        if username and password:
            # 判断用户是否存在
            buyer = Buyer.objects.filter(username=username).first()
            if buyer:
                # 密码加密比对
                web_password = setPassword(password)
                if web_password == buyer.password:
                    response = HttpResponseRedirect('/Buyer/index/')
                    response.set_cookie("username",buyer.username)
                    request.session["username"] = buyer.username
                    # 在下发一个user_id的信息方便其他功能查询
                    response.set_cookie("user_id",buyer.id)
                    return response
    return render(request,"buyer/login.html")
# v2.6 登录校验装饰器
def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

# v2.6 前台用户首页
# @loginValid
def index(request):
    goods_type_list = GoodsType.objects.all()
    return render(request,"buyer/index.html",locals())

# v2.6 前台用户注销
def logout(request):
    response = HttpResponseRedirect('/Buyer/login/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response



def base(request):
    return render(request,"buyer/base.html")