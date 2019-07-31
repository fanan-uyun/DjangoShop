"""
    当前文件只是为了规定接口的模型及数据字段
"""
from rest_framework import serializers

from Store.models import *

# Serializers define the API representation.
class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    """
    声明查询的表和要返回的字段
    """
    # 定义元类
    class Meta:
        # 要进行接口序列化的模型
        model = Goods
        # 序列化返回的字段
        fields = ['goods_name','goods_price','goods_number','goods_date','goods_safeDate','id']


# Serializers define the API representation.
class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    声明查询的表和要返回的字段
    """
    # 定义元类
    class Meta:
        # 要进行接口序列化的模型
        model = GoodsType
        # 序列化返回的字段
        fields = ['name','description']