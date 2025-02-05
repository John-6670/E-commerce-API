from django.contrib import admin

from .models import ProductCategory, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'created_at', 'updated_at']
    list_filter = ['category']
    search_fields = ['name', 'desc']
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
