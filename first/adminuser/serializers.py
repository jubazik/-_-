from rest_framework import serializers
from django.db import transaction
from .models import Category, Type, Products, Order, OrderItem, PaymentOrder, CashReceiptOrder, DisbursementCashOrder
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['user']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']
        read_only_fields = ['user']


class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    is_available = serializers.BaseSerializer(read_only=True)
    display_price = serializers.CharField(read_only=True)

    class Meta:
        model = Products
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'type', 'type_name', 'user', 'is_available', 'display_price'
        ]
        read_only_fields = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'product_price', 'count', 'price', 'sum', 'user']
        read_only_fields = ['price', 'sum', 'user']

        def validate(self, data):
            # Проверяем что товар принадлежит тому же пользователю
            if data['product'].user != self.context['request'].user:
                raise serializers.ValidationError('Товар не принадлежит текущему пользователю ')
            # Проверяем, что товар доступен

            if not data['product'].is_availadle():
                raise serializers.ValidationError('Товар недоступен для заказа')

            if data['count'] <= 0:
                raise serializers.ValidationError('Количество должно быть больше 0')

            return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    product_list = serializers.CharField(read_only=True)
    status_displey = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'number', 'date', 'status', 'status_display', 'user',
            'total_sum', 'products_list', 'items'
        ]

        read_only_fields = ['number', 'date', 'user', 'total_sum', 'products_list']

        def create(self, validated_data):
            item_data = validated_data.pop('item', [])
            user = self.context["request"].user
            while transaction.atomic():
                order = Order.objects.create(user=user, **validated_data)
                for item_data in item_data:
                    OrderItem.objects.create(order=order, user=user, **item_data)
            return order

        def update(self, instance, validated_data):
            item_data = validated_data.pop('item', None)
            with transaction.atomic():
                # Обновляем основные поля заказа
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()

                # если переданы item, обновляем их
                if item_data is not None:
                    # Удаляем существующие item
                    instance.orderitem_set.all().delete()

                    # Создаем новый items
                    for item_data in item_data:
                        OrderItem.objects.create(
                            order=instance,
                            user=instance.user,
                            **item_data
                        )
            return instance


class CashReceiptOrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.number", read_only=True)
    order_date = serializers.DateField(source="order.date", read_only=True)

    class Meta:
        model = CashReceiptOrder
        fields = ['id', 'number', 'date', 'order', 'order_number', 'order_date', 'sum', 'user']
        read_only_fields = ['number', 'date', 'sum', 'user']

    def validated_order(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('Заказ не принадлежит текущему пользователю')

        if value.status != 'cash':
            raise serializers.ValidationError("Кассовы ордер можно создать только для оплаченного наличными заказа")

        return value


class PaymentOrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.number', read_only=True)
    order_date = serializers.DateField(source='order.date', read_only=True)

    class Meta:
        model = PaymentOrder
        fields = ['id', 'date', 'order', 'order_number', 'order_date', 'sum', 'user']
        read_only_fields = ['number', 'date', 'sum', 'user']

    def validated_order(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('Заказа не принадлежит текущему пользователю')
        if value.status != 'without_cash':
            raise serializers.ValidationError('Платежно поручение можно создать только для безналичного заказа')
        return value

    class CategoryListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = ['id', 'name']

    class TypeListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Type
            fields = ['id', 'name']

    class ProductsListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Products
            fields = ['id', 'name', 'price', 'is_aveilable']


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'number', 'date', 'status', 'status_display', 'total_sum']


class DisbursementCashOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisbursementCashOrder
        fields = [
            'id', 'number_order', 'date', 'sum_'
        ]
        read_only_fields = ['user']


