[![](https://img.shields.io/badge/python-3.6.3-orange.svg)](https://www.python.org/downloads/release/python-363/)
[![](https://img.shields.io/badge/django-2.1.8-green.svg)](https://docs.djangoproject.com/en/2.1/releases/2.1/)
[![](https://img.shields.io/badge/jQuery-3.3.1-blue.svg)](https://code.jquery.com/jquery-3.3.1.min.js/)
[![](https://img.shields.io/badge/Bootstrap-4.3.1-mauve.svg)](https://getbootstrap.com/)

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


**3、前后端用户名重复校验**

后端（针对登录功能）

```python
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
```

效果图：

![](https://github.com/py304/DjangoShop/blob/master/images/loginerror.jpg)


前端校验（针对注册功能）

```python
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
```

注册页面添加如下内容：

```html
<script>
      $("#username").blur(
          function () {
              var username = $("#username").val();
              var csrfmiddlewaretoken = '{{ csrf_token }}';
              var url = "/Store/ajax/";
              send_data = {
                  "username":username,
                  "csrfmiddlewaretoken":csrfmiddlewaretoken
              };
              $.ajax(
                  {
                      url: url,
                      type: "post",
                      data: send_data,
                      success: function (data) {
                          var status = data.status;
                          $("#sign").text(data.data);
                          if(status == "error"){
                              $("#submit").attr("disabled",true)
                          }else {
                              $("#submit").attr("disabled",false)
                          }
                          {#alert(data.data)#}
                          {#console.log(data)#}
                      },
                      error: function (error) {
                          console.log(error)
                      }
                  }
              )
          }
      )

  </script>

```

效果图：

![](https://github.com/py304/DjangoShop/blob/master/images/regerror.jpg)


## 三、编写退出功能（删除cookie）

定义视图函数：

```python
# 退出功能（删除cookie)
def exit(request):
    response = HttpResponseRedirect("/Store/login/")
    response.delete_cookie("username")
    del request.session["username"]
    return response

```

更改首页logout超链接的href为/Store/exit/

![](https://github.com/py304/DjangoShop/blob/master/images/exit.jpg)


## 四、编写base模板页，其他页面继承模板页

```html
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>{% block title %}{% endblock %}</title>

  <!-- Custom fonts for this template-->
  <link href="/static/store/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">

  <!-- Custom styles for this template-->
  <link href="/static/store/css/sb-admin-2.min.css" rel="stylesheet">
  {% block style %}{% endblock %}

</head>

<body id="page-top">

  <!-- Page Wrapper -->
  <div id="wrapper">

    <!-- Sidebar -->
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
        <div class="sidebar-brand-icon rotate-n-15">
          <i class="fas fa-laugh-wink"></i>
        </div>
        <div class="sidebar-brand-text mx-3">后台管理系统</div>
      </a>

      <!-- Divider -->
      <hr class="sidebar-divider my-0">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item">
        <a class="nav-link" href="index.html">
          <i class="fas fa-fw fa-tachometer-alt"></i>
          <span>店铺管理</span></a>
      </li>

      <!-- Divider -->
      <hr class="sidebar-divider">

      <!-- Heading -->
      <div class="sidebar-heading">
        销售管理
      </div>

      <!-- Nav Item - Pages Collapse Menu -->
      <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
          <i class="fas fa-fw fa-cog"></i>
          <span>商品管理</span>
        </a>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <h6 class="collapse-header">定制组件:</h6>
            <a class="collapse-item" href="buttons.html">按钮</a>
            <a class="collapse-item" href="cards.html">卡片</a>
          </div>
        </div>
      </li>

      <!-- Nav Item - Utilities Collapse Menu -->
      <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseUtilities" aria-expanded="true" aria-controls="collapseUtilities">
          <i class="fas fa-fw fa-wrench"></i>
          <span>工具</span>
        </a>
        <div id="collapseUtilities" class="collapse" aria-labelledby="headingUtilities" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <h6 class="collapse-header">定制工具:</h6>
            <a class="collapse-item" href="utilities-color.html">颜色</a>
            <a class="collapse-item" href="utilities-border.html">边框</a>
            <a class="collapse-item" href="utilities-animation.html">动画</a>
            <a class="collapse-item" href="utilities-other.html">其他</a>
          </div>
        </div>
      </li>

      <!-- Divider -->
{#      <hr class="sidebar-divider">#}

      <!-- Nav Item - Charts -->
{#      <li class="nav-item">#}
{#        <a class="nav-link" href="charts.html">#}
{#          <i class="fas fa-fw fa-chart-area"></i>#}
{#          <span>图表</span></a>#}
{#      </li>#}

      <!-- Nav Item - Tables -->
{#      <li class="nav-item">#}
{#        <a class="nav-link" href="tables.html">#}
{#          <i class="fas fa-fw fa-table"></i>#}
{#          <span>表格</span></a>#}
{#      </li>#}

      <!-- Divider -->
{#      <hr class="sidebar-divider d-none d-md-block">#}

      <!-- Sidebar Toggler (Sidebar) -->
      <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
      </div>

    </ul>
    <!-- End of Sidebar -->

    <!-- Content Wrapper -->
    <div id="content-wrapper" class="d-flex flex-column">

      <!-- Main Content -->
      <div id="content">

        <!-- Topbar -->
        <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

          <!-- Sidebar Toggle (Topbar) -->
          <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
            <i class="fa fa-bars"></i>
          </button>

          <!-- Topbar Search -->
          <form class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
            <div class="input-group">
              <input type="text" class="form-control bg-light border-0 small" placeholder="搜索" aria-label="Search" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button class="btn btn-primary" type="button">
                  <i class="fas fa-search fa-sm"></i>
                </button>
              </div>
            </div>
          </form>

          <!-- Topbar Navbar -->
          <ul class="navbar-nav ml-auto">

            <!-- Nav Item - Search Dropdown (Visible Only XS) -->
            <li class="nav-item dropdown no-arrow d-sm-none">
              <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-search fa-fw"></i>
              </a>
              <!-- Dropdown - Messages -->
              <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in" aria-labelledby="searchDropdown">
                <form class="form-inline mr-auto w-100 navbar-search">
                  <div class="input-group">
                    <input type="text" class="form-control bg-light border-0 small" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2">
                    <div class="input-group-append">
                      <button class="btn btn-primary" type="button">
                        <i class="fas fa-search fa-sm"></i>
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </li>

            <!-- Nav Item - Alerts -->
            <li class="nav-item dropdown no-arrow mx-1">
              <a class="nav-link dropdown-toggle" href="#" id="alertsDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-bell fa-fw"></i>
                <!-- Counter - Alerts -->
                <span class="badge badge-danger badge-counter">3+</span>
              </a>
              <!-- Dropdown - Alerts -->
              <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="alertsDropdown">
                <h6 class="dropdown-header">
                  警报中心
                </h6>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="mr-3">
                    <div class="icon-circle bg-primary">
                      <i class="fas fa-file-alt text-white"></i>
                    </div>
                  </div>
                  <div>
                    <div class="small text-gray-500">2019年12月12日</div>
                    <span class="font-weight-bold">一份新的月报已准备好下载!</span>
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="mr-3">
                    <div class="icon-circle bg-success">
                      <i class="fas fa-donate text-white"></i>
                    </div>
                  </div>
                  <div>
                    <div class="small text-gray-500">2019年12月7日</div>
                    290.29美元已存入您的账户!
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="mr-3">
                    <div class="icon-circle bg-warning">
                      <i class="fas fa-exclamation-triangle text-white"></i>
                    </div>
                  </div>
                  <div>
                    <div class="small text-gray-500">2019年12月2日<</div>
                    消费提醒:我们注意到您的账户消费异常高.
                  </div>
                </a>
                <a class="dropdown-item text-center small text-gray-500" href="#">显示所有警报</a>
              </div>
            </li>

            <!-- Nav Item - Messages -->
            <li class="nav-item dropdown no-arrow mx-1">
              <a class="nav-link dropdown-toggle" href="#" id="messagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-envelope fa-fw"></i>
                <!-- Counter - Messages -->
                <span class="badge badge-danger badge-counter">7</span>
              </a>
              <!-- Dropdown - Messages -->
              <div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="messagesDropdown">
                <h6 class="dropdown-header">
                  消息中心
                </h6>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="dropdown-list-image mr-3">
                    <img class="rounded-circle" src="https://source.unsplash.com/fn_BT9fwg_E/60x60" alt="">
                    <div class="status-indicator bg-success"></div>
                  </div>
                  <div class="font-weight-bold">
                    <div class="text-truncate">嘿，你好！我想知道你是否能帮我解决一个我一直遇到的问题.</div>
                    <div class="small text-gray-500">Emily Fowler · 58m</div>
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="dropdown-list-image mr-3">
                    <img class="rounded-circle" src="https://source.unsplash.com/AU4VPcFN4LE/60x60" alt="">
                    <div class="status-indicator"></div>
                  </div>
                  <div>
                    <div class="text-truncate">我有你上个月订购的照片，你想怎么寄给你?</div>
                    <div class="small text-gray-500">Jae Chun · 1d</div>
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="dropdown-list-image mr-3">
                    <img class="rounded-circle" src="https://source.unsplash.com/CS2uCrpNzJY/60x60" alt="">
                    <div class="status-indicator bg-warning"></div>
                  </div>
                  <div>
                    <div class="text-truncate">上个月的报告看起来不错，我很高兴到目前为止取得的进展，继续做好工作!</div>
                    <div class="small text-gray-500">Morgan Alvarez · 2d</div>
                  </div>
                </a>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <div class="dropdown-list-image mr-3">
                    <img class="rounded-circle" src="https://source.unsplash.com/Mv9hjnEUHR4/60x60" alt="">
                    <div class="status-indicator bg-success"></div>
                  </div>
                  <div>
                    <div class="text-truncate">我是个好孩子吗?我问这个问题是因为有人告诉我，人们对所有的狗都这么说，即使它们并不好...</div>
                    <div class="small text-gray-500">Chicken the Dog · 2w</div>
                  </div>
                </a>
                <a class="dropdown-item text-center small text-gray-500" href="#">阅读更多信息</a>
              </div>
            </li>

            <div class="topbar-divider d-none d-sm-block"></div>

            <!-- Nav Item - User Information -->
            <li class="nav-item dropdown no-arrow">
              <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <span class="mr-2 d-none d-lg-inline text-gray-600 small">{{ request.COOKIES.username }}</span>
                <img class="img-profile rounded-circle" src="https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=4001431513,4128677135&fm=26&gp=0.jpg">
              </a>
              <!-- Dropdown - User Information -->
              <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="userDropdown">
                <a class="dropdown-item" href="#">
                  <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                  个人中心
                </a>
                <a class="dropdown-item" href="#">
                  <i class="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                  系统设置
                </a>
                <a class="dropdown-item" href="#">
                  <i class="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                  登录日志
                </a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="#" data-toggle="modal" data-target="#logoutModal">
                  <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                  注销
                </a>
              </div>
            </li>

          </ul>

        </nav>
        <!-- End of Topbar -->

        <!-- Begin Page Content -->

        <!-- /.container-fluid -->
        {% block content %}

        {% endblock %}

      </div>
      <!-- End of Main Content -->

      <!-- Footer -->
      <footer class="sticky-footer bg-white">
        <div class="container my-auto">
          <div class="copyright text-center my-auto">
            <span>Copyright &copy; Your Website 2019</span>
          </div>
        </div>
      </footer>
      <!-- End of Footer -->

    </div>
    <!-- End of Content Wrapper -->

  </div>
  <!-- End of Page Wrapper -->

  <!-- Scroll to Top Button-->
  <a class="scroll-to-top rounded" href="#page-top">
    <i class="fas fa-angle-up"></i>
  </a>

  <!-- Logout Modal-->
  <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">准备离开?</h5>
          <button class="close" type="button" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">×</span>
          </button>
        </div>
        <div class="modal-body">如果您准备结束当前会话，请选择下面的“注销”.</div>
        <div class="modal-footer">
          <button class="btn btn-secondary" type="button" data-dismiss="modal">取消</button>
          <a class="btn btn-primary" href="login.html">注销</a>
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

  {% block script %}
  
  {% endblock %}

</body>

</html>
```


## 五、店铺注册

在首页功能视图函数中判断用户是否有店铺，通过Store类中user_id

```python
# 首页
@loginValid
def index(request):
    """
    v1.5 添加检测账号是否有店铺的逻辑
    """
    # 查询当前用户
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    # 通过用户查询店铺是否存在（店铺和用户通过用户的id进行关联）
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,"store/index.html",{"is_store":is_store})

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
```

前端base也添加判断

```html
      <li class="nav-item">
        {% if is_store == 1 %}
        <a class="nav-link" href="index.html">
          <i class="fas fa-fw fa-tachometer-alt"></i>
                <span>店铺管理</span></a>
        {% else %}
        <a class="nav-link" href="/Store/store_register/">
          <i class="fas fa-fw fa-tachometer-alt"></i>
                <span>没有店铺，注册一个</span></a>
        {% endif %}

      </li>
```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/dian.jpg)

指定一个注册店铺的前端页

```html
{% extends "store/base.html" %}

{% block title %}
    后台管理首页
{% endblock %}

        {% block content %}
        <form class="form" method="post" enctype="multipart/form-data">
            <div class="form-group">
                {% csrf_token %}
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="store_name" placeholder="店铺名称">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="store_address" placeholder="店铺地址">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="store_description" placeholder="店铺描述">
            </div>
            <div class="form-group">
                <input type="file" class="form-control form-control-user"  name="store_logo" placeholder="店铺logo">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="store_phone" placeholder="店铺电话">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="store_money" placeholder="店铺注册资金">
            </div>
            <div class="form-group">
                <select name="type" class="form-control form-control-user" multiple="multiple">
                    {% for t in type_list %}
                        <option value="{{ t.id }}">{{ t.store_type }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="form-group">
                <input class="btn btn-primary btn-block" type="submit" value="注册">
            </div>
        </form>
        {% endblock %}

```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/store_reg.jpg)


完善注册店铺视图函数：

```python
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


    return render(request,"store/store_register.html",locals())
```


![](https://github.com/py304/DjangoShop/blob/master/images/rr.jpg)


![](https://github.com/py304/DjangoShop/blob/master/images/store_data.jpg)



## 六、添加商品

前端页面：

```html
{% extends "store/base.html" %}

{% block title %}
    后台管理首页
{% endblock %}

        {% block content %}
        <form class="form" method="post" enctype="multipart/form-data">
            <div class="form-group">
                {% csrf_token %}
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="goods_name" placeholder="商品名称">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="goods_price" placeholder="商品价格">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="goods_image" placeholder="商品图片">
            </div>
            <div class="form-group">
                <input type="file" class="form-control form-control-user"  name="goods_number" placeholder="商品库存">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="goods_description" placeholder="商品描述">
            </div>

            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="goods_date" placeholder="出厂日期">
            </div>
            <div class="form-group">
                <input type="text" class="form-control form-control-user"  name="goods_safeDate" placeholder="保质期(月)">
            </div>
            <div class="form-group">
                <input type="hidden" class="form-control form-control-user"  name="store_id" value="1">
            </div>
            <div class="form-group">
                <input class="btn btn-primary btn-block" type="submit" value="添加">
            </div>
        </form>
        {% endblock %}


```

后端业务视图：

```python
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


    return render(request,"store/add_goods.html")
```

![](https://github.com/py304/DjangoShop/blob/master/images/add_goods.jpg)


## 七、商品列表

前端：

```html
{% extends "store/base.html" %}

{% block title %}
    商品列表页面
{% endblock %}

{% block label %}
    <a class="btn btn-warning" href="/Store/add_good/">添加商品</a>
{% endblock %}

{% block content %}
    <table class="table-bordered table">
        <thead>
            <tr>
                <th>商品名称</th>
                <th>商品价格</th>
                <th>商品数量</th>
                <th>出厂日期</th>
                <th>保质期</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            {% for goods in goods_list %}
            <tr>
                <td>{{ goods.goods_name }}</td>
                <td>{{ goods.goods_price }}</td>
                <td>{{ goods.goods_number }}</td>
                <td>{{ goods.goods_date }}</td>
                <td>{{ goods.goods_safeDate }}</td>
                <td>
                    <a class="btn btn-danger" href="#">下架</a>
                    <a class="btn btn-primary" href="#">销毁</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

```

后端：

```python
# v1.7 展示商品列表
def list_goods(request):
    # v1.7 查询所有商品信息(提前添加了商品数据)
    goods_list = Goods.objects.all()
    return render(request,"store/goods_list.html",locals())
```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/goods_list.jpg)


## 八、添加商品列表搜索功能

前端：

![](https://github.com/py304/DjangoShop/blob/master/images/search.jpg)

后端：

```python
# v1.7 展示商品列表
def list_goods(request):
    # v1.8 添加keywords关键字字段，用户前端搜索
    keywords = request.GET.get("keywords","")
    if keywords:
        # v1.8 对关键字进行模糊查询
        goods_list = Goods.objects.filter(goods_name__contains=keywords)
    else:
        # v1.7 查询所有商品信息(提前添加了商品数据)
        goods_list = Goods.objects.all()
    return render(request,"store/goods_list.html",locals())
```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/search_g.jpg)

## 九、商品列表页搜索分页功能

后端：

```python
# v1.7 展示商品列表
def list_goods(request):
    # v1.8 添加keywords关键字字段，用户前端搜索
    keywords = request.GET.get("keywords","")
    # v1.9 获取前端页码,默认页码1
    page_num = request.GET.get("page_num",1)
    if keywords:
        # v1.8 对关键字进行模糊查询
        goods_list = Goods.objects.filter(goods_name__contains=keywords)
    else:
        # v1.7 查询所有商品信息(提前添加了商品数据)
        goods_list = Goods.objects.all()
    # v1.9 新增列表分页功能，创建分页器,针对good_list中的数据，每页3条数据
    paginator = Paginator(goods_list,3)
    # v1.9 获取具体页的数据
    page = paginator.page(int(page_num))
    # v1.9 返回页码列表
    page_range = paginator.page_range
    # 返回分页数据
    return render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords})
```

前端：

```html
{% extends "store/base.html" %}

{% block title %}
    商品列表页面
{% endblock %}

{% block label %}
    <a class="btn btn-warning" href="/Store/add_good/">添加商品</a>
{% endblock %}

{% block content %}
    <table class="table-bordered table">
        <thead>
            <tr align="center">
                <th>商品名称</th>
                <th>商品价格</th>
                <th>商品数量</th>
                <th>出厂日期</th>
                <th>保质期</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
{#            {% for goods in goods_list %}#}
            {% for goods in page %}
            <tr align="center">
                <td>{{ goods.goods_name }}</td>
                <td>
                    <input type="text" value="{{ goods.goods_price }}" style="text-align: center">
                </td>
                <td>{{ goods.goods_number }}</td>
                <td>{{ goods.goods_date }}</td>
                <td>{{ goods.goods_safeDate }}</td>
                <td>
                    <a class="btn btn-danger" href="#">下架</a>
                    <a class="btn btn-primary" href="#">销毁</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="dataTables_paginate paging_simple_numbers">
        <ul class="pagination">
            {% for p in page_range %}
            <li class="paginate_button page-item ">
                <a class="page-link" href="?keywords={{ keywords }}&page_num={{ p }}">{{ p }}</a>
            </li>
            {% endfor %}
        </ul>
    </div>
{% endblock %}
```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/page.jpg)





## 九、商品详情页添加

**1、新建一个商品详情页面goods.html**

```html
{% extends "store/base.html" %}

{% block title %}
    {{ goods_data.goods_name }} 详情
{% endblock %}

{% block content %}
    <table class="table">
        <tr>
            <td rowspan="3">
                <img style="width: 200px;height: 200px;" src="/static/{{ goods_data.goods_image }}">
            </td>
            <th>
                商品名称
            </th>
            <td colspan="3">
                {{ goods_data.goods_name }}
            </td>
        </tr>

        <tr>
            <th>
                商品价格
            </th>
            <td>
                {{ goods_data.goods_price }}
            </td>
            <th>
                商品库存
            </th>
            <td>
                {{ goods_data.goods_number }}
            </td>
        </tr>

        <tr>
            <th>
                生产日期
            </th>
            <td>
                {{ goods_data.goods_date }}
            </td>
            <th>
                保质期
            </th>
            <td>
                {{ goods_data.goods_safeDate }}
            </td>
        </tr>

        <tr>
            <th colspan="5" style="text-align: center;">商品描述</th>
        </tr>
        <tr>
            <td colspan="5">{{ goods_data.goods_description }}</td>
        </tr>
    </table>
    <a class="btn btn-primary btn-block" href="#">修改商品信息</a>
{% endblock %}
```

**2、视图，路由**

![](https://github.com/py304/DjangoShop/blob/master/images/goods.jpg)


**3、在列表页绑定路由**

![](https://github.com/py304/DjangoShop/blob/master/images/goods_a.jpg)

**4、通过点击商品列表中的商品跳转到商品详情页**

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/goods_s.jpg)


## 十、商品信息修改功能实现

**1、新建一个前端修改商品信息页面update_goods.html**

```html
{% extends "store/base.html" %}

{% block title %}
    {{ goods_data.goods_name }} 详情
{% endblock %}

{% block content %}
    <form class="form" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <table class="table">
        <tr>
            <td rowspan="3">
                <img style="width: 200px;height: 200px;" src="/static/{{ goods_data.goods_image }}">
                <input class="form-control form-control-user" type="file" name="goods_image">
            </td>
            <th>
                商品名称
            </th>
            <td colspan="3">
                <input class="form-control form-control-user" type="text" name="goods_name" value="{{ goods_data.goods_name }}">
            </td>
        </tr>

        <tr>
            <th>
                商品价格
            </th>
            <td>
                <input class="form-control form-control-user" type="text" name="goods_price" value="{{ goods_data.goods_price }}">
            </td>
            <th>
                商品库存
            </th>
            <td>
                <input class="form-control form-control-user" type="text" name="goods_number" value="{{ goods_data.goods_number }}">
            </td>
        </tr>

        <tr>
            <th>
                生产日期
            </th>
            <td>
                <input class="form-control form-control-user" type="text" name="goods_date" value="{{ goods_data.goods_date }}">
            </td>
            <th>
                保质期
            </th>
            <td>
                <input class="form-control form-control-user" type="text" name="goods_safeDate" value="{{ goods_data.goods_safeDate }}">
            </td>
        </tr>

        <tr>
            <th colspan="5" style="text-align: center;">商品描述</th>
        </tr>
        <tr>
            <td colspan="5">
                <textarea class="form-control form-control-user" name="goods_description">
                    {{ goods_data.goods_description }}
                </textarea>
            </td>
        </tr>

        <tr>
            <td colspan="5" style="text-align: center;">
                <input class="btn btn-primary btn-block" type="submit" value="保存修改">
            </td>
        </tr>
    </table>
    </form>
{% endblock %}
```

**2、后端简单视图及路由添加和商品详细类似，展示效果**

![](https://github.com/py304/DjangoShop/blob/master/images/update.jpg)


**3、使用富文本编辑器修改商品描述**

修改setting配置

![](https://github.com/py304/DjangoShop/blob/master/images/ckeditor_app.jpg)

![](https://github.com/py304/DjangoShop/blob/master/images/ckeditor_set.jpg)

修改主url

![](https://github.com/py304/DjangoShop/blob/master/images/ckeditor_url.jpg)

**4、收集静态文件（注意注释配置，收集后，在回复配置）**

![](https://github.com/py304/DjangoShop/blob/master/images/sj.jpg)


**5、前端导入富文本js文件，并应用到商品描述**

```html
{# v2.1 导入ckeditor js文件，并应用到商品描述#}
{% block script %}
    <script src="/static/ckeditor/ckeditor/ckeditor.js"></script>
    <script>
        CKEDITOR.replace("goods_description",{uiColor:"#9AB8F3"})
    </script>
{% endblock %}
```

效果：

![](https://github.com/py304/DjangoShop/blob/master/images/save.jpg)

**6、视图添加数据修改保存操作**

![](https://github.com/py304/DjangoShop/blob/master/images/update_view.jpg)

修改界面：

![](https://github.com/py304/DjangoShop/blob/master/images/update_xj.jpg)

修改信息后跳转商品详情：

![](https://github.com/py304/DjangoShop/blob/master/images/update_xjx.jpg)


## 十一、校验用户是否有商铺功能

**1、在用户登录时下发校验店铺的cookie**

![](https://github.com/py304/DjangoShop/blob/master/images/store_cookie.jpg)

**2、在base页重新进行前端店铺校验**

```html
    <!-- Sidebar -->
    {% if request.COOKIES.is_store %}
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
        <div class="sidebar-brand-icon rotate-n-15">
          <i class="fas fa-laugh-wink"></i>
        </div>
        <div class="sidebar-brand-text mx-3">后台管理系统</div>
      </a>

      <!-- Divider -->
      <hr class="sidebar-divider my-0">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item">
{#        {% if is_store %}#}
        <a class="nav-link" href="#">
          <i class="fas fa-fw fa-tachometer-alt"></i>
                <span>店铺管理</span></a>
{#        {% else %}#}
{#        <a class="nav-link" href="/Store/store_register/">#}
{#          <i class="fas fa-fw fa-tachometer-alt"></i>#}
{#                <span>没有店铺，注册一个</span></a>#}
{#        {% endif %}#}

      </li>

      <!-- Divider -->
      <hr class="sidebar-divider">

      <!-- Heading -->
      <div class="sidebar-heading">
        销售管理
      </div>

      <!-- Nav Item - Pages Collapse Menu -->
      <li class="nav-item">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
          <i class="fas fa-fw fa-cog"></i>
          <span>商品管理</span>
        </a>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
          <div class="bg-white py-2 collapse-inner rounded">
            <h6 class="collapse-header">商品信息:</h6>
            <a class="collapse-item" href="/Store/add_good/">添加商品</a>
            <a class="collapse-item" href="/Store/goods_list/">商品列表</a>
          </div>
        </div>
      </li>

      <!-- Nav Item - Utilities Collapse Menu -->

      <!-- Divider -->
{#      <hr class="sidebar-divider">#}

      <!-- Nav Item - Charts -->
{#      <li class="nav-item">#}
{#        <a class="nav-link" href="charts.html">#}
{#          <i class="fas fa-fw fa-chart-area"></i>#}
{#          <span>图表</span></a>#}
{#      </li>#}

      <!-- Nav Item - Tables -->
{#      <li class="nav-item">#}
{#        <a class="nav-link" href="tables.html">#}
{#          <i class="fas fa-fw fa-table"></i>#}
{#          <span>表格</span></a>#}
{#      </li>#}

      <!-- Divider -->
{#      <hr class="sidebar-divider d-none d-md-block">#}

      <!-- Sidebar Toggler (Sidebar) -->
      <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
      </div>

    </ul>
    <!-- End of Sidebar -->
    {% else %}
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
        <div class="sidebar-brand-icon rotate-n-15">
          <i class="fas fa-laugh-wink"></i>
        </div>
        <div class="sidebar-brand-text mx-3">后台管理系统</div>
      </a>

      <!-- Divider -->
      <hr class="sidebar-divider my-0">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item">
        <a class="nav-link" href="/Store/store_register/">
          <i class="fas fa-fw fa-tachometer-alt"></i>
                <span>没有店铺，注册一个</span></a>
      </li>

      <!-- Divider -->
      <hr class="sidebar-divider">

      <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
      </div>

    </ul>
    {% endif %}
```

**3、后端更新装饰器店铺cookie下发并装饰到店铺注册函数视图上**

![](https://github.com/py304/DjangoShop/blob/master/images/valid_up.jpg)


效果展示：

![](https://github.com/py304/DjangoShop/blob/master/images/none.jpg)

![](https://github.com/py304/DjangoShop/blob/master/images/none1.jpg)

![](https://github.com/py304/DjangoShop/blob/master/images/none2.jpg)


## 十二、业务逻辑实现：查看商品列表是针对当前用户的店铺

**1、更改添加商品页面的店铺id为自动获取cookie，每次添加商品的时候就会自动关联当前页面cookie中的店铺id**

```html
    <div class="form-group">
        <input type="hidden" class="form-control form-control-user"  name="store_id" value="{{ request.COOKIES.is_store }}">
    </div>
```

**2、修改后端商品列表视图，使用多对多关系反向查询**

![](https://github.com/py304/DjangoShop/blob/master/images/current_good.jpg)


![](https://github.com/py304/DjangoShop/blob/master/images/current_list.jpg)


## 十三、商品下架功能

**1、商品模型类添加商品状态字段,并同步数据库**

```python
# v2.4 新增商品状态字段;1 待售 0 下架
    goods_under = models.IntegerField(verbose_name="商品状态",default=1)
```

**2、更改商品列表视图，是查询上架商品**

![](https://github.com/py304/DjangoShop/blob/master/images/under.jpg)


**3、新增商品下架视图函数**

```python
# v2.4 新增商品上架功能
def under_goods(request):
    id = request.GET.get("id")
    # v2.4 返回当前请求的来源地址
    referer = request.META.get("HTTP_REFERER")
    if id:
        # v2.4 获取指定id的商品
        goods = Goods.objects.filter(id=id).first()
        # v2.4 修改商品状态
        goods.goods_under = 0
        goods.save()
    return HttpResponseRedirect(referer)
```

**4、更新商品列表前端页面下架标签**

```html
<a class="btn btn-danger" href="/Store/goods_under/?id={{ goods.id }}">下架</a>
```



## 十三、商品上架及销毁功能














