from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet, ReviewViewSet


router = DefaultRouter()
router.register('all', ProductViewSet, basename='product')  # Empty prefix for products
router.register('categories', ProductCategoryViewSet, basename='category')  # Explicit route for categories

urlpatterns = [
    path('', include(router.urls)),
    path('all/<slug:product_slug>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('all/<slug:product_slug>/reviews/<int:pk>/', ReviewViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'}), name='review-detail'),
]
