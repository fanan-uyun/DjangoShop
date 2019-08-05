import time

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.db.models import Sum

from Buyer.models import *
from Store.models import *
from Store.views import setPassword


from alipay import AliPay # v3.3 导入支付宝支付接口模块

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

from django.views.decorators.cache import cache_page

@cache_page(60*15)  # 对当前视图进行缓存,缓存的寿命是15分钟
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


# v3.4 商品详情页功能视图，通过get参数获取
def goods_detail(request):
    goods_id = request.GET.get("goods_id")
    if goods_id:
        goods = Goods.objects.filter(id=int(goods_id)).first()
        if goods:
            return render(request, "buyer/detail.html",locals())
    return HttpResponse("没有您指定的商品")

# v3.5 订单号生成函数
def setOrder(user_id,goods_id,store_id):
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strtime+str(user_id)+str(goods_id)+str(store_id)

# v3.5 订单详情
def place_order(request):
    # 判断商品详情页加入购买后的提交方式
    if request.method == "POST":
        # 商品详情页添加了两个input
        # post数据
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        # cookie数据
        user_id = request.COOKIES.get("user_id")
        # 数据库数据
        goods = Goods.objects.get(id=int(goods_id))
        # store_id = goods.store_id.get(id = 7).id
        # v3.6 更替商铺商品一对多关系字段保存商铺id
        store_id = goods.store_id.id
        price = goods.goods_price

        # 创建一个订单
        order = Order()
        order.order_id = setOrder(user_id,goods_id,store_id)
        order.goods_count = count
        order.order_user = Buyer.objects.get(id=user_id)
        order.order_price = count * price
        # v3.7 添加订单状态字段
        order.order_status = 1
        order.save()

        # 创建订单详情
        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods_id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count * goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image = goods.goods_image
        order_detail.save()
        # 因为order_detail可能不止一个商品，所以使用列表存储
        detail = [order_detail]
        return render(request,"buyer/place_order.html",locals())
    else:
        order_id = request.GET.get("order_id")
        if order_id:
            order = Order.objects.get(id=order_id)
            detail = order.orderdetail_set.all()
            return render(request, "buyer/place_order.html", locals())
        return HttpResponse("非法请求")

# v3.8 购物车列表页展示
def cart(request):
    # 根据cookie获取user_id
    user_id = request.COOKIES.get("user_id")
    # 查询购物车中的商品
    goods_list = Cart.objects.filter(user_id = user_id)
    # v4.0 购物车商品添加至订单列表
    if request.method == "POST":
        # 获取购物车页面请求的post数据
        post_data = request.POST
        # 此列表用于收集前端传过来的商品
        cart_data = []
        cart_list_id = []
        # 遍历post数据，将购物车列表商品信息取出来
        for k,v in post_data.items():
            # 前端input选择框定义了name和value为购物车对应id
            if k.startswith("goods_"):
                cart_data.append(Cart.objects.get(id=int(v)))
                # v4.1 将购物车id存储到cart_list_id中
                cart_list_id.append(int(v))

        # 提交过来的购物车数据总数（不是商品数量）
        goods_count = len(cart_data)
        # 订单总价
        # goods_total = sum([int(i.goods_total) for i in cart_data])
        # v4.1 使用聚类查询计算总价
        cart_goods = Cart.objects.filter(id__in=cart_list_id).aggregate(Sum("goods_total"))
        # {'goods_total__sum': 258.0}
        goods_total = cart_goods.get("goods_total__sum")

        # 保存订单
        order = Order()
        # 购物车中生成订单号时，订单中可能有多个商品或多个商铺；使用goods_count代替商品id，使用一个数字代替商铺id
        order.order_id = setOrder(user_id,goods_count,"2")
        order.goods_count = goods_count
        order.order_user = Buyer.objects.get(id=user_id)
        order.order_price = goods_total
        order.order_status = 1
        order.save()

        # 保存订单详情,这里的cart是购物车里的数据实例，不是商品的实例
        for cart in cart_data:
            orderdetail = OrderDetail()
            orderdetail.order_id = order
            orderdetail.goods_id = cart.goods_id
            orderdetail.goods_name = cart.goods_name
            orderdetail.goods_price = cart.goods_price
            orderdetail.goods_number = cart.goods_number
            orderdetail.goods_total = cart.goods_total
            orderdetail.goods_store = cart.goods_store
            orderdetail.goods_image = cart.goods_picture
            orderdetail.save()
        # 当在购物车中点击“"去结算"时跳转到订单列表进行支付
        url = "/Buyer/place_order/?order_id=%s"%order.id
        return HttpResponseRedirect(url)

    return render(request,"buyer/cart.html",locals())

# v3.8 添加购物车
def add_cart(request):
    # 定义json数据状态
    result = {"state":"error","data":""}
    if request.method == "POST":
        # 获取ajax_post请求数据
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        # 数据库查询商品
        goods = Goods.objects.get(id=int(goods_id))
        # 根据cookie查询当前用户
        user_id = request.COOKIES.get("user_id")

        # 创建一个购物车，用于添加数据
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price * count
        cart.goods_number = count
        cart.goods_picture = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.id
        cart.user_id = user_id
        cart.save()
        result["state"] = "success"
        result["data"] = "商品添加成功"
    else:
        result["data"] = "请求错误"
    return JsonResponse(result)

# v4.1 删除购物车中的商品
def del_cart_goods(request):
    cart_id = request.GET.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    referer = request.META.get("HTTP_REFERER")
    cart.delete()
    return HttpResponseRedirect(referer)

# v3.3 将支付宝接口应用到前台付款,并用get请求发送支付金额和订单id
def pay_order(request):
    # v3.3 获取订单金额
    money = request.GET.get("money")
    # v3.3 获取订单id
    order_id = request.GET.get("order_id")
    # v3.2 定义变量存储支付宝应用公钥
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv66JqpsopyoXYMiWiIgyV4O/nc4ptXjRgZO9dkKRzsh1LusdILASoXlZ65nx/4ONCDpFn5QEQQNerVtmCW+Y9N/GmNnQOsEeX5tCxfNlg7vHS5Hk8QDCgIbEzVC3K+9wwYiCc8aQRjSM+Czb/Tq3kI+XJpDIGE6lPtp2zkwZaPt3y8yt88MpYcqPllNn3acEW8U5LnQmMHosohqlXu5iPK57OC7a0oC5AwUPlZcMizO2EqmxonWpfqk+scOhVdyVUwuX6siye76OkUuhO8M1758hhhNOUhmzhurEEW20toqA2eoMP63GweyTt5kWmWcqc30YU0FAN8Aq3QG03wF3xQIDAQAB
    -----END PUBLIC KEY-----"""
    # v3.2 定义变量存储支付宝应用私钥
    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAv66JqpsopyoXYMiWiIgyV4O/nc4ptXjRgZO9dkKRzsh1LusdILASoXlZ65nx/4ONCDpFn5QEQQNerVtmCW+Y9N/GmNnQOsEeX5tCxfNlg7vHS5Hk8QDCgIbEzVC3K+9wwYiCc8aQRjSM+Czb/Tq3kI+XJpDIGE6lPtp2zkwZaPt3y8yt88MpYcqPllNn3acEW8U5LnQmMHosohqlXu5iPK57OC7a0oC5AwUPlZcMizO2EqmxonWpfqk+scOhVdyVUwuX6siye76OkUuhO8M1758hhhNOUhmzhurEEW20toqA2eoMP63GweyTt5kWmWcqc30YU0FAN8Aq3QG03wF3xQIDAQABAoIBAHSkuL+qJcX79jf+OKSjBMd+s/dKwtTczdklV5EEl4gXMkA38QS4QM4kc5TMnJgZrJQKKd4fC6uoak/iI6iwUYsKNedD/NQUOvCBIdQl9muAtJmHEaObC8F8wXwTlzPURHBxKrlbZuZiCjrnyYNC3PvKdXeReUJZcXNbLBsD8h6QgVOPaKXnLCSTZf98gHXkDN0IWlNp08143b4Xp6DO+CiaUHUbUrAcHdB+gHQJnN3+YP3dnVGzvyRisjJ8B8mTS1zPk4fpciViA6EMCYLHFCrS+8LZ+WEpJN8o/0o9Mgpd8YPKg1q4WDlYp1ulnRUVqOkJaVZVOvecTtbPbyaJWUECgYEA9fj7peww3VmPNYS3WAAtm/M5YMgsuFNRWC61/o+FKDSVlH57dVRRTnnGF7NE5dUHldloAa+yBw5Zbi/s5LjYV36zvga4dYZpA8Lt4uglzg3QAXwQ+X5YRqkde1gGolOdU/MsnhvehQpdOoZ5XWzJHe/2kA8RNraZyYsER0PQ2hECgYEAx373L2VZZdhPT8EIrgrAU93izxZAS9Cp5A/whogxmVhaKfGHcJa4YygajzyKd3DRoSmYtbXqysGXZyY+RmolCyMeZEBZ1s/2DTj2vtdh3ngV6UQY4vbgpCBgDCOnoiAq/5whcFcTDjma79BmsdHng/ZXgo+5U6v4TrKdZ7ay7nUCgYEArEZnkk175/xLFjPO6d6uExTmMgfhcnRAe9+zbgh9PayeuzNfKs0UaT9W49CWR9bNikGL2+p/aPu+3TLJ22QvehBuuYAhf4bVVGIZlRv9JnV8Ix4PEX9ROqRF1tbPRrADeAHQVSi10D5zD4ORy0JfFg20hi9XYhfAXG12YKd5xtECgYB8t3A6ziZsWCWFG42cmJYSGDYx9pwtiX6cWCarRDuVvTlo3Vkp1t/hBXJNN7Ds6Lf1A/c3KkplhU9sqejmxnbwFn1qeRxxAcO2EnWXazkBBpvUH8FbKrHXiXHiROwInAmlkOsKuzTrgLHO2L9KzYnp4rhkpAtdNrZeJKXo77u+/QKBgF4DmigjHYR32dmKXZQYp2DkM7lFxnuL6McR0r/5b/wkMUPSInCK4n4e8vBH611dkaNNhNSTR5aVsrMZuBGzQrFOGnXawa+PxpGPaVwR/jf/tPCLmsq2KPenQPF15tc+4dosMp726+f+4Klg71qMK8yjGN+fkrHo3Er1y+35Letj
    -----END RSA PRIVATE KEY-----"""

    # v3.2 实例化支付应用
    alipay = AliPay(
        appid="2016101000652510",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # v3.2 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # v3.3 订单号
        total_amount=str(money),  # v3.3 支付金额
        subject="生鲜交易",  # 交易主题暂时固定成“"生鲜交易"
        # v3.3 支付完成要跳转的本地路由
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",
        # v3.3 支付完成要跳转的异步路由
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/"
    )
    # v3.7 添加支付成功后订单状态置为2待发货
    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()
    # v3.3 发起购买商品跳转支付路由
    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

# v3.3 编写接收支付结果的视图，用于支付结束后前台网站给用户的响应页面
def pay_result(request):
    """
    收集了一下支付宝支付成功自动用get请求返回的参数：
    # 编码
    charset=utf-8
    # 订单号
    out_trade_no=10001
    # 订单类型
    method=alipay.trade.page.pay.return
    # 订单金额
    total_amount=1200.00
    # 校验值
    sign=OqHkG0OypYgrTL%2Fu%2FJbZi1DaSHEhxOPEu1KRVWOF9IrDoUYpTw7P4mVZni2SOgsXWOxiET%2BaODHBOwk1qpu0T8P58OK41Ajv6Scy6KoEpi5USDL1Q0765i5EMTD4ei3x9tUzG07Wl9EWqKNk4Y3gFLfMdcsKJy%2BOF2aFdOyuO1UXJSRlSzg2HIz9ozR40BkHEHy7TH1Updnc7nOWDH4NCkowPQN0g8HSfX6shdfImvaSGHLC5rzMfmfFPlyEjy7HGuQ7u3APP2SZNCGTQKzE58NXD3w4tLGCJBl5nfmwgdWz3kUA0J9wWAzpZ7J0btdtBV7h1kOQAx9pWYJK%2BVvDAA%3D%3D
    # 系统订单号
    trade_no=2019072622001414251000021352
    # 用户的应用id
    auth_app_id=2016101000652510
    # 版本
    version=1.0
    # 商家的应用id
    app_id=2016101000652510
    # 加密方式
    sign_type=RSA2
    # 商家id
    seller_id=2088102178922754
    # 时间
    timestamp=2019-07-26+19%3A59%3A37
    """
    return render(request,"buyer/pay_result.html",locals())
    # return HttpResponse("支付成功")





def base(request):
    return render(request,"buyer/base.html")