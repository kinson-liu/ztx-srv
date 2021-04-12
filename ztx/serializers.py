from rest_framework import serializers
from .models import Costomer, Product, Income, Trade

class CostomerSerializer(serializers.ModelSerializer):
    """
    客户序列化
    """
    class Meta:
        model = Costomer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    产品序列化
    """
    class Meta:
        model = Product
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    """
    收入序列化
    """
    costomer_name = serializers.CharField(source="costomer.name")
    product_name = serializers.CharField(source="type",read_only=True)
    class Meta:
        model = Income
        fields = ['id','create_time','update_time','type','costomer_name','money','product_name']


class TradeSerializer(serializers.ModelSerializer):
    """
    交易序列化
    """
    costomer_name = serializers.CharField(source="costomer.name",read_only= True)
    product_name = serializers.CharField(source="product.name",read_only= True)
    # price = serializers.CharField(source="product.price",read_only= True)
    costomer_id = serializers.IntegerField(write_only= True)
    product_id = serializers.IntegerField(write_only= True)
    class Meta:
        model = Trade
        fields = ['id','create_time','update_time','product_name','costomer_name','product_id','costomer_id','price']
