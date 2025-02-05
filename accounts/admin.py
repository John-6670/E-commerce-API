from django.contrib import admin

from .models import CustomUser, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)
    list_display = ('full_name', 'email', 'phone_number', 'date_of_birth', 'national_id')
    list_display_links = ('full_name', 'email')
    search_fields = ('full_name', 'email', 'phone_number', 'national_id')
    list_filter = ('date_of_birth', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number')}),
        ('Personal info', {
            'classes': ('collapse',),
            'fields': ('first_name', 'last_name', 'national_id', 'date_of_birth')
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important dates', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined', 'last_login')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'street_address', 'postal_code', 'default')
    list_display_links = ('user', 'country')
    search_fields = ('user__username', 'user__email', 'country', 'city', 'street_address', 'postal_code')
    list_filter = ('country', 'city', 'default')
    fieldsets = (
        (None, {'fields': ('user', 'country', 'city', 'street_address')}),
        ('Advanced Fields', {'fields': ('apartment_address', 'postal_code')}),
        ('Default', {
            'classes': ('collapse',),
            'fields': ('default',)
        }),
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
