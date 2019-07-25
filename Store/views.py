import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator  # v1.9 导入分页模块


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
                    # v1.5 添加下发user_id的cookie
                    response.set_cookie("user_id", seller.id)
                    request.session["username"] = seller.username
                    # v2.2 新增下发是否有店铺的cookie
                    # v2.2 先查询店铺是否存在
                    store = Store.objects.filter(user_id=seller.id).first()
                    # v2.2 再下发cookie
                    if store:
                        response.set_cookie("is_store",store.id)
                    else:
                        response.set_cookie("is_store","")
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
# def loginValid(fun):
#     def inner(request,*args,**kwargs):
#         # 获取成功登录后的cookie和session
#         c_user = request.COOKIES.get("username")
#         s_user = request.session.get("username")
#         # 如果cookie和session都存在并且值都相同
#         if c_user and s_user and c_user == s_user:
#             # 通过c_user查询数据库
#             seller = Seller.objects.filter(username=c_user).first()
#             # 如果有这个用户，则返回函数，这里只index
#             if seller:
#                 # v2.2 获取当前页面cookie中的user_id
#                 user_id = request.COOKIES.get("user_id")
#                 # v2.2 被装饰函数返回作为一个响应(这里意思：先保存店铺）
#                 response = fun(request, *args, **kwargs)
#                 # v2.2 通过该user_id去查询该用户有无店铺(再去查询有无该店铺)
#                 store = Store.objects.filter(user_id=int(user_id)).first()
#                 # 判断店铺是否存在，进行相应的cookie下发，这里注意cookie下发之后，如果是数字，不论是0还是false都为字符串类型，都是True
#                 if store:
#                     response.set_cookie("is_store",store.id)
#                 else:
#                     response.set_cookie("is_store","")
#                 return response
#         # 否则重定向到登录页面
#         return HttpResponseRedirect("/Store/login/")
#     return inner



def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Store/login/")
    return inner

# 首页
@loginValid
def index(request):
    """
    v1.5 添加检测账号是否有店铺的逻辑
    """
    # 查询当前用户
    # user_id = request.COOKIES.get("user_id")
    #     # if user_id:
    #     #     user_id = int(user_id)
    #     # else:
    #     #     user_id = 0
    #     # # 通过用户查询店铺是否存在（店铺和用户通过用户的id进行关联）
    #     # store = Store.objects.filter(user_id=user_id).first()
    #     # if store:
    #     #     is_store = store.id
    #     # else:
    #     #     is_store = ""
    return render(request,"store/index.html")

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
    for key in request.COOKIES: # 获取当前所有cookie
        response.delete_cookie(key)
    del request.session["username"]
    return response

@loginValid
def store_register(request):
    # v1.5 新增店铺注册
    # 查询所有的店铺类型
    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST #接收post数据
        # print(request.FILES)
        # print(post_data)
        store_name = post_data.get("store_name")
        store_address = post_data.get("store_address")
        store_description = post_data.get("store_description")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")

        # 通过cookie来获得user_id
        user_id = int(request.COOKIES.get("user_id"))
        # 通过request.post得到类型数据，是个列表
        type_lsts = post_data.getlist("type")
        # 通过request.FILES获取上传的图片
        store_logo = request.FILES.get("store_logo")

        # 保存正常数据
        store = Store()
        store.store_name = store_name
        store.store_address = store_address
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()

        # 在生成数据中添加多对多关系字段
        for i in type_lsts:# 循环type列表，得到类型id
            store_type = StoreType.objects.get(id=i)#查询类型数据
            store.type.add(store_type)# 添加到类型字段，多对多的映射表
        store.save()
        # 数据保存成功后跳转到主页
        response = HttpResponseRedirect('/Store/index/')
        # 下发cookie证明当前用户有店铺
        response.set_cookie("is_store",store.id)
        return response

    return render(request,"store/store_register.html",locals())

# v1.6添加商品
def add_goods(request):
    if request.method == "POST":
        # v1.6 获取前端post请求数据
        good_postData = request.POST
        # v1.6 通过前端name字段获取实际的值存储起来
        goods_name = good_postData.get("goods_name")
        goods_price = good_postData.get("goods_price")
        goods_number = good_postData.get("goods_number")
        goods_description = good_postData.get("goods_description")
        goods_date = good_postData.get("goods_date")
        goods_safeDate = good_postData.get("goods_safeDate")
        # v1.6 注意图片是通过FILES方式获取
        goods_image = request.FILES.get("goods_image")
        # v1.6 多对多关系字段，前端使用隐藏域
        store_id = good_postData.get("store_id")

        # 保存正常数据
        goods = Goods() # 实例化一个商品对象
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save() # 保存一条记录

        # 保存多对多数据(注意get方式获取到的数据为字符串)
        goods.store_id.add(
            Store.objects.get(id=int(store_id))
        )
        goods.save()
        return HttpResponseRedirect('/Store/goods_list/up/')

    return render(request,"store/add_goods.html")

# v1.7 展示商品列表 v2.5 新增上下架页面参数
def list_goods(request,state):
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    # v1.8 添加keywords关键字字段，用户前端搜索
    keywords = request.GET.get("keywords","")
    # v1.9 获取前端页码,默认页码1
    page_num = request.GET.get("page_num",1)
    # v2.3 查询店铺
    store_id = request.COOKIES.get("is_store")
    store = Store.objects.get(id=int(store_id))
    if keywords:
        # v1.8 对关键字进行模糊查询
        # goods_list = Goods.objects.filter(goods_name__contains=keywords)
        # v2.3 使用多对多关系查询，查询当前商铺的商品
        # v2.4 新增商品状态查询字段，前端只显示上架商品
        goods_list = store.goods_set.filter(goods_name__contains=keywords,goods_under=state_num)
    else:
        # v1.7 查询所有商品信息(提前添加了商品数据)
        # goods_list = Goods.objects.all()
        # goods_list = store.goods_set.all()
        goods_list = store.goods_set.filter(goods_under=state_num)
    # v1.9 新增列表分页功能，创建分页器,针对good_list中的数据，每页3条数据
    paginator = Paginator(goods_list,3)
    # v1.9 获取具体页的数据
    page = paginator.page(int(page_num))
    # v1.9 返回页码列表
    page_range = paginator.page_range
    # 返回分页数据
    return render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords,"store_name":store.store_name,"state":state})

# def list_goods(request):
#     """
#     商品的列表页
#     :param request:
#     :return:
#     """
#     #完成了模糊查询
#     keywords = request.GET.get("keywords","")
#     page_num = request.GET.get("page_num",1)
#     referer = request.META.get("HTTP_REFERER")
#     if keywords:
#         goods_list = Goods.objects.filter(goods_name__contains=keywords)
#     else:
#         if referer and "?" in referer:
#             get_str = referer.split("?")[1]
#             get_list = [i.split("=") for i in get_str.split("&")]
#             get_dict = dict(get_list)
#             get_dict["keywords"] = get_dict["keywords"].encode()
#             if "keywords" in get_dict:
#                 keywords = get_dict["keywords"]
#             goods_list = Goods.objects.filter(goods_name__contains=keywords)
#         else:
#             goods_list = Goods.objects.all()
#     #完成分页查询
#     paginator = Paginator(goods_list,3)
#     page = paginator.page(int(page_num))
#     page_range = paginator.page_range
#
#     return render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords})


# v2.0 新增展示商品详情页功能
def goods(request, goods_id):
    # v2.0 这里通过前端传递一个商品id来查询该商品信息
    goods_data = Goods.objects.filter(id=goods_id).first()
    return render(request,"store/goods.html",locals())

# v2.1 新增修改商品信息页面功能
def update_goods(request, goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        # v2.1 获取前端post请求数据
        good_postData = request.POST
        # v2.1 通过前端name字段获取实际的值存储起来
        goods_name = good_postData.get("goods_name")
        goods_price = good_postData.get("goods_price")
        goods_number = good_postData.get("goods_number")
        goods_description = good_postData.get("goods_description")
        goods_date = good_postData.get("goods_date")
        goods_safeDate = good_postData.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")

        # v2.1开始修改商品信息
        goods = Goods.objects.get(id=int(goods_id)) # v2.1 获取当前商品信息
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image: # v2.1 如果有上传图片在发起修改
            goods.goods_image = goods_image
        goods.save() # 保存当前修改的数据
        # v2.1 修改成功后重定向到商品详情页面
        return HttpResponseRedirect('/Store/goods/%s/'%goods_id)

    return render(request, "store/update_goods.html", locals())


# v2.4 新增商品上架功能
def set_goods(request,state):
    # v2.5 使该视图同时具备上下架及销毁的功能
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id")
    # v2.4 返回当前请求的来源地址
    referer = request.META.get("HTTP_REFERER")
    if id:
        # v2.4 获取指定id的商品
        goods = Goods.objects.filter(id=id).first()
        # v2.5 判断前端路由中的字段参数来进行相应的操作，这里如果为delete，删除该商品
        if state == "delete":
            goods.delete()
        else:
            # v2.4 修改商品状态
            goods.goods_under = state_num
            goods.save()
    return HttpResponseRedirect(referer)
