from django.urls import path

from .views import CartView, OrderView, AddCartItemView


urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddCartItemView.as_view(), name='cart-add-item'),
]
