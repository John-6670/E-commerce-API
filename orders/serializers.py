from rest_framework import serializers

from .models import Order, Cart, CartItem, Payment


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'total', 'status', 'created_at']
        read_only_fields = ['total']

    def validate_status(self, value):
        if value not in self.Meta.model.Status:
            raise serializers.ValidationError('Status is wrong')
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'status', 'created_at']

    def validate_status(self, value):
        if value not in self.Meta.model.Status:
            raise serializers.ValidationError('Status is wrong')
        return value

    def create(self, validated_data):
        order = validated_data['order']
        order.status = Order.Status.COMPLETED
        order.save()

        payment = Payment.objects.create(**validated_data)
        return payment
