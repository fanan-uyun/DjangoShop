from django.contrib import admin
from Store import models
# Register your models here.
admin.site.register(models.Store)
admin.site.register(models.Goods)
admin.site.register(models.GoodsType)
admin.site.register(models.StoreType)
admin.site.register(models.Seller)
admin.site.register(models.GoodsImg)