from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg

from .utils import generate_unique_slug

User = get_user_model()


def product_image_path(instance, filename):
    return f"product/images/{instance.name}/{filename}"


def get_default_product_category():
    return ProductCategory.objects.get_or_create(name="Others")[0].id


class ProductCategory(models.Model):
    name = models.CharField(_('Category name'), max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    desc = models.TextField(_("Description"), blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET(get_default_product_category),
                                 default=get_default_product_category, related_name='product_list')
    discount = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_discount_range",
                check=models.Q(discount__range=(0, 100)),
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def rate(self):
        return self.reviews.aggregate(average_rate=Avg('rate'))['average_rate'] or 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_rate_range",
                check=models.Q(rate__range=(1, 5)),
            ),
        ]

    def __str__(self):
        return f'Review by {self.user} for {self.product}'
