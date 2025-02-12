from rest_framework import serializers

from .models import Product, ProductCategory, ProductImage, Review


class ProductCategorySerializer(serializers.ModelSerializer):
    parent = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True, lookup_field='slug')

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, lookup_field='slug')

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
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True, lookup_field='slug')
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'desc', 'price', 'stock', 'category', 'discount', 'images', 'reviews', 'rate', 'created_at', 'updated_at']
        lookup_field = 'slug'

    def get_rate(self, obj):
        return obj.rate

    def validate(self, data):
        discount = data.get('discount', 0)
        if not 0 <= discount <= 100:
            raise serializers.ValidationError('Discount must be between 0 and 100.')

        stock = data.get('stock', 1)
        if stock < 0:
            raise serializers.ValidationError('Stock must be greater than or equal to 0.')

        return data
