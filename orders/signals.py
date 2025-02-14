from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Cart, Order

User = get_user_model()


@receiver(post_migrate, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Cart.objects.create(user=instance)
