from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Order, Cart, Payment, ShippingAddress, CartItem
from .serializers import OrderSerializer, CartSerializer, PaymentSerializer, ShippingAddressSerializer, CartItemSerializer
from products.models import Product


class CartView(generics.RetrieveUpdateAPIView, mixins.RetrieveModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart = self.queryset.get(user=self.request.user)
        if hasattr(cart, 'order'):
            self.check_object_permissions(self.request, cart)
            return cart
        return cart

    def put(self, request, *args, **kwargs):
        cart = self.get_object()
        if hasattr(cart, 'order'):
            raise PermissionDenied("You cannot edit the cart after an order has been created.")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        cart = self.get_object()
        if hasattr(cart, 'order'):
            raise PermissionDenied("You cannot edit the cart after an order has been created.")
        return self.partial_update(request, *args, **kwargs)


class AddCartItemView(generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({"detail": "Item added to cart."}, status=status.HTTP_200_OK)



class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
