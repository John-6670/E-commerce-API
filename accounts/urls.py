from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_blacklist

from .views import ProfileRetrieveUpdateView, AddressViewSet, RegisterView, EmailVerificationView, SendVerificationEmailView


router = DefaultRouter()
router.register('addresses', AddressViewSet)

urlpatterns = [
    path('profile/', ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('logout/', token_blacklist, name='logout'),
    path('send-verification-email/', SendVerificationEmailView.as_view(), name='send-verification-email'),
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email-verify'),
]
urlpatterns += router.urls
