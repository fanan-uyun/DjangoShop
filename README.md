[![](https://img.shields.io/badge/python-3.6.3-orange.svg)](https://www.python.org/downloads/release/python-363/)
[![](https://img.shields.io/badge/django-2.1.8-green.svg)](https://docs.djangoproject.com/en/2.1/releases/2.1/)
[![](https://img.shields.io/badge/jQuery-3.3.1-blue.svg)](https://code.jquery.com/jquery-3.3.1.min.js/)

# Django电商项目

## 一、环境配置
**1、创建Django项目**

django-admin startproject DjangoShop

**2、创建App（Store店铺）**

python manage.py startapp Store

**3、创建App下模板目录及静态文件目录**

![static](https://github.com/py304/DjangoShop/blob/master/images/static.jpg)


**4、创建主static目录用于收集静态文件**


**5、setting文件设置**

- 安装App
- STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

- MEDIA_URL = '/media/'
- MEDIA_ROOT = os.path.join(BASE_DIR,'static')

- STATIC_ROOT = os.path.join(BASE_DIR,'static')

收集静态文件时注释STATICFILES_DIRS、MEDIA_URL、MEDIA_ROOT

收集完成取消上述三个注释，再注释STATIC_ROOT

## 二、创建数据模型类

**1、创建模型**
```python
from django.db import models

# Create your models here.
# 定义卖家模型类
class Seller(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    nickname = models.CharField(max_length=32,verbose_name="昵称",null=True,blank=True)
    phone = models.CharField(max_length=32,verbose_name="手机",null=True,blank=True)
    email = models.EmailField(verbose_name="邮箱",null=True,blank=True)
    picture = models.ImageField(upload_to="store/images",verbose_name="头像",null=True,blank=True)
    address = models.CharField(max_length=32,verbose_name="地址",null=True,blank=True)

    card_id = models.CharField(max_length=32,verbose_name="身份证",null=True,blank=True)

# 定义店铺类型类
class StoreType(models.Model):
    store_type = models.CharField(max_length=32,verbose_name="类型名称")
    type_description = models.TextField(verbose_name="类型描述")

# 定义店铺类
class Store(models.Model):
    store_name = models.CharField(max_length=32,verbose_name="店铺名称")
    store_address = models.CharField(max_length=32,verbose_name="店铺地址")
    store_description = models.TextField(verbose_name="店铺描述")
    store_logo = models.ImageField(upload_to="store/images",verbose_name="店铺logo")
    store_phone = models.CharField(max_length=32,verbose_name="店铺电话")
    store_money = models.FloatField(verbose_name="店铺注册资金")

    user_id = models.IntegerField(verbose_name="店铺主人")
    type = models.ManyToManyField(to=StoreType,verbose_name="店铺类型")

# 定义商品类
class Goods(models.Model):
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_image = models.ImageField(upload_to="store/images",verbose_name="商品图片")
    goods_number = models.IntegerField(verbose_name="商品库存")
    goods_description = models.TextField(verbose_name="商品描述")
    goods_date = models.DateField(verbose_name="出厂日期")
    goods_safeDate = models.IntegerField(verbose_name="保质期")

    store_id = models.ManyToManyField(to=Store,verbose_name="商品店铺")

# 定义商品图片类
class GoodsImg(models.Model):
    img_address = models.ImageField(upload_to="store/images",verbose_name="图片地址")
    img_description = models.TextField(verbose_name="图片描述")
    goods_id = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name="商品id")

    
```

**2、同步数据库**

校验配置

python manage.py check

生成数据库语句

python manage.py makemigrations

同步数据库

python manage.py migrate

收集静态文件
python manage.py collectstatic(收集完成注意恢复配置，并注释STATIC_ROOT)


## 三、创建登录注册功能

**1、编写注册登录功能**

将模板中的注册HTML文件复制到App下templates-store下

![reg](https://github.com/py304/DjangoShop/blob/master/images/reg_temp.jpg)

编写简单视图显示页面

![](https://github.com/py304/DjangoShop/blob/master/images/sim_view.jpg)

创建独立url

![](https://github.com/py304/DjangoShop/blob/master/images/sub_url.jpg)

填写主url

![](https://github.com/py304/DjangoShop/blob/master/images/main_url.jpg)

更改原html文档，将所有css,js导入路径更改为/static/store/...,在访问网页

![](https://github.com/py304/DjangoShop/blob/master/images/template.jpg)

改动HTML布局

```html
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>SB Admin 2 - Register</title>

  <!-- Custom fonts for this template-->
  <link href="/static/store/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">

  <!-- Custom styles for this template-->
  <link href="/static/store/css/sb-admin-2.min.css" rel="stylesheet">

</head>

<body class="bg-gradient-primary">

  <div class="container">

    <div class="card o-hidden border-0 shadow-lg my-5">
      <div class="card-body p-0">
        <!-- Nested Row within Card Body -->
        <div class="row">
          <div class="col-lg-5 d-none d-lg-block bg-register-image"></div>
          <div class="col-lg-7">
            <div class="p-5">
              <div class="text-center">
                <h1 class="h4 text-gray-900 mb-4">注册用户</h1>
              </div>
              <form class="user" method="post">
					{% csrf_token %}
                <div class="form-group">
                  <input type="text" class="form-control form-control-user" name="username" placeholder="用户名">
                </div>
                <div class="form-group">
                  <input type="password" class="form-control form-control-user" name="password" placeholder="密码">
                </div>
                <div class="form-group">
                  <input type="submit" class="btn btn-primary btn-user btn-block" value="注册">
                </div>
{#                <a href="login.html" class="btn btn-primary btn-user btn-block">#}
{#                  Register Account#}
{#                </a>#}
                <hr>
{#                <a href="index.html" class="btn btn-google btn-user btn-block">#}
{#                  <i class="fab fa-google fa-fw"></i> Register with Google#}
{#                </a>#}
{#                <a href="index.html" class="btn btn-facebook btn-user btn-block">#}
{#                  <i class="fab fa-facebook-f fa-fw"></i> Register with Facebook#}
{#                </a>#}
              </form>
              <hr>
              <div class="text-center">
                <a class="small" href="forgot-password.html">忘记密码?</a>
              </div>
              <div class="text-center">
                <a class="small" href="login.html">已经有账户了? 登录!</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Bootstrap core JavaScript-->
  <script src="/static/store/vendor/jquery/jquery.min.js"></script>
  <script src="/static/store/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

  <!-- Core plugin JavaScript-->
  <script src="/static/store/vendor/jquery-easing/jquery.easing.min.js"></script>

  <!-- Custom scripts for all pages-->
  <script src="/static/store/js/sb-admin-2.min.js"></script>

</body>

</html>
```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/register.jpg)

复制register文档做登录页面并编写完整注册视图函数：

```python
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
```


测试注册功能

![](https://github.com/py304/DjangoShop/blob/master/images/test.jpg)

**2、完善登录功能**

在登录页面下发cookie，在登录请求校验cookie。如果登录成功，则跳转到首页；否则跳转登录页面

先布局index首页（复制模板当中的index页面并修改样式路径）

![](https://github.com/py304/DjangoShop/blob/master/images/index_temp.jpg)

完善登录视图：

```python
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

# 首页
def index(request):
    return render(request,"store/index.html",locals())
```

效果图：

![](https://github.com/py304/DjangoShop/blob/master/images/index.jpg)

做个装饰器，给首页添加校验功能，没有cookie不能直接登录首页，只有用户登录成功才能进入首页

```python
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

```

现在直接进入index首页会自动跳转至登录页面

![](https://github.com/py304/DjangoShop/blob/master/images/valid.jpg)















