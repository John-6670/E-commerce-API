from django.contrib import admin

from .models import CustomUser, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'date_of_birth', 'is_staff']
    list_filter = ['is_staff', 'date_of_birth']
    search_fields = ['username', 'email', 'full_name']
    inlines = [AddressInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
