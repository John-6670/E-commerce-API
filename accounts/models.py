from email.policy import default

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('Email Address'), null=True, blank=True, unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=13, null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=10, null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return None

    def __str__(self):
        return self.full_name or self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='addresses')
    country = models.CharField(max_length=100, default='Iran')
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        self.country = self.country.title()
        self.city = self.city.title()
        self.street_address = self.street_address.title()
        super().save(*args, **kwargs)
