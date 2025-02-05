from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
from accounts.models import Address

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_item')
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.cart.user}"


class Order(models.Model):
    class Status(models.TextChoices):
        AWAITING_PENDING = 'A', 'Awaiting payment'
        COMPLETED = 'p', 'paid'
        CANCELLED = 'X', 'Cancelled'
        DELIVERED = 'D', 'Delivered'
        SHIPPED = 'S', 'Shipped'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
    total = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.AWAITING_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def save(self, *args, **kwargs):
        self.total = sum(item.product.price * item.quantity for item in self.cart.items.all())
        super().save(*args, **kwargs)


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'
        FAILED = 'F', 'Failed'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='payments', null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Payment for order {self.order.id}"

    def save(self, *args, **kwargs):
        self.amount = self.order.total
        super().save(*args, **kwargs)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Shipping address for order {self.order.id}"
