from rest_framework import generics, permissions, mixins, status, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Order, Cart, Payment, CartItem
from .serializers import OrderSerializer, CartSerializer, PaymentSerializer, CartItemSerializer
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

        cart = Cart.objects.get(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if product.stock < quantity:
            return Response({"detail": "Requested quantity not available."}, status=status.HTTP_400_BAD_REQUEST)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        product.stock -= quantity
        product.save()

        return Response({"detail": "Item added to cart."}, status=status.HTTP_201_CREATED)


class RemoveCartItemView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            product.stock += cart_item.quantity
            product.save()
            cart_item.delete()
            return Response({"detail": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order_id = self.kwargs['pk']
        try:
            order = Order.objects.get(id=order_id, user=self.request.user)
        except Order.DoesNotExist:
            raise PermissionDenied("You cannot create a payment for another user's order.")
        serializer.save(order=order)


class CompletePaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            payment = Payment.objects.get(order_id=pk, user=request.user)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        payment.status = Payment.Status.COMPLETED
        payment.save()

        payment.order.status = Order.Status.COMPLETED
        payment.order.save()

        return Response({"detail": "Payment completed and order status updated to Paid."}, status=status.HTTP_200_OK)
