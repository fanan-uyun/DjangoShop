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

