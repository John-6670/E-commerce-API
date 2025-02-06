from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_blacklist

from . views import ProfileRetrieveUpdateView, AddressViewSet


router = DefaultRouter()
router.register('addresses', AddressViewSet)

urlpatterns = [
    path('profile/', ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('logout/', token_blacklist, name='logout'),
]
urlpatterns += router.urls
