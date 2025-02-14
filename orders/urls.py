from django.urls import path

from .views import CartView, OrderView, AddCartItemView, PaymentCreateAPIView, CompletePaymentView


urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddCartItemView.as_view(), name='cart-add-item'),
    path('orders/<int:pk>/payment/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('orders/<int:pk>/pay/', CompletePaymentView.as_view(), name='payment-complete'),
]
