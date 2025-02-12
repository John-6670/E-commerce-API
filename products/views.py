from rest_framework import viewsets, permissions
from rest_framework.generics import RetrieveAPIView

from .models import Product, ProductCategory, Review
from .serializers import ProductSerializer, ProductCategorySerializer, ReviewSerializer
from accounts.permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        return Review.objects.filter(product__slug=product_slug)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
