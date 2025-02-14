from django.contrib import admin

from .models import Cart, CartItem, Order, Payment


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__username', 'user__email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'total', 'status', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('status',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'created_at')
    search_fields = ('order__user__username', 'order__user__email')
    list_filter = ('status',)
