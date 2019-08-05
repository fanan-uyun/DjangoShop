from django_filters import rest_framework as filters
from Store.models import *
from rest_framework import generics

class GoodsFilter(filters.FilterSet):
    goods_name = filters.CharFilter(field_name='goods_name', lookup_expr='icontains',label="模糊查询商品名")
    min_price = filters.NumberFilter(field_name="goods_price", lookup_expr='gte',label="查询最低金额")
    max_price = filters.NumberFilter(field_name="goods_price", lookup_expr='lte',label="查询最高金额")

    class Meta:
        model = Goods
        fields = ['goods_name', 'min_price','max_price']