from rest_framework import serializers
from .models import CashReceiptOrder, Category, Products, Type, Order, OrderItem, PaymentOrder

class TypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ["name"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CategorySerializers(serializers.ModelSerializer):
    class MetaL:
        model = Category
        fields = ['name']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "name", "description", "price", "category", "type"
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderItemSet(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(),
        source='product',
        write_only=True,
        required=True
    )
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'count', 'price', 'sum']
        read_only_fields = ['price', 'sum']



# class OrderSerializers(serializers.ModelSerializer):
#     products = Products.objects.all()
#
#
#
#     class Meta:
#         model = Order
#         fields = ['date', 'table', 'status']
#         read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        return super().create(validated_data)



    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



