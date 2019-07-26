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
    # v3.0 定义一个容器用来存放结果
    result_list = []
    # v2.9 查询所有商品类型
    goods_type_list = GoodsType.objects.all()
    # v3.0 循环类型
    for goods_type in goods_type_list:
        # v3.0 这个查询出来是个QuerySet列表套字典类型，但是前面的商品类型没有对应，所有手动构建数据
        goods_list = goods_type.goods_set.values()[:4]  # 取前4条商品信息
        if goods_list:# 如果类型有对应的商品
            # v3.0 构建输出结果
            goodsType = {
                "id":goods_type.id,
                "name":goods_type.name,
                "description":goods_type.description,
                "picture":goods_type.picture,
                "goods_list":goods_list
            }
            # v3.0 查询商品类型当中有数据的数据，将有数据的类型及数据放入定义的列表中
            result_list.append(goodsType)
    return render(request,"buyer/index.html",locals())

# v2.6 前台用户注销
def logout(request):
    response = HttpResponseRedirect('/Buyer/login/')
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response

# v3.1 前台商品列表展示
def goods_list(request):
    """
    前台列表页
    :param request:
    :return:
    """
    goodsList = []
    type_id = request.GET.get("type_id")
    # v3.1 获取商品类型
    goods_type = GoodsType.objects.filter(id = type_id).first()
    if goods_type:
        # v3.1 查询所有上架的产品
        goodsList = goods_type.goods_set.filter(goods_under=1)
    return render(request,"buyer/goods_list.html",locals())

def base(request):
    return render(request,"buyer/base.html")