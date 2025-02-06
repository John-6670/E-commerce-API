from rest_framework import serializers

from .models import Product, ProductCategory, ProductImage, Review


# TODO: create view for parent field in ProductCategorySerializer
class ProductCategorySerializer(serializers.ModelSerializer):
    parent = serializers.HyperlinkedRelatedField(view_name='product-category-detail', read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rate', 'comment', 'created_at']

    def get_user(self, obj):
        return obj.user.username

    def validate_rate(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rate must be between 0 and 5.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.HyperlinkedRelatedField(view_name='product-category-detail', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'desc', 'price', 'stock', 'category', 'discount', 'images', 'reviews', 'rate', 'created_at', 'updated_at']

    def get_rate(self, obj):
        return obj.rate

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Discount must be between 0 and 100.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be greater than or equal to 0.")
        return value
