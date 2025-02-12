from rest_framework import serializers

from .models import Order, Cart, CartItem, Payment, ShippingAddress


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, lookup_field='slug')

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

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Cart must have at least one item")
        return value


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='profile', read_only=True)
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'total', 'status', 'created_at']
        read_only_fields = ['total']

    def validate_status(self, value):
        if value not in self.Meta.model.Status:
            raise serializers.ValidationError('Status is wrong')
        return value

    def create(self, validated_data):
        cart_data = validated_data.pop('cart')
        cart_items_data = cart_data.pop('items')

        cart = Cart.objects.create(**cart_data)
        for item_data in cart_items_data:
            CartItem.objects.create(cart=cart, **item_data)

        order = Order.objects.create(cart=cart, **validated_data)
        return order

class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.HyperlinkedRelatedField(view_name='order-detail', read_only=True)

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


class ShippingAddressSerializer(serializers.ModelSerializer):
    order = serializers.HyperlinkedRelatedField(view_name='order-detail', read_only=True)

    class Meta:
        model = ShippingAddress
        fields = ['id', 'order', 'address', 'city', 'state', 'zip_code', 'country', 'created_at']

    def create(self, validated_data):
        order = validated_data['order']
        shipping_address = ShippingAddress.objects.create(**validated_data)
        return shipping_address
