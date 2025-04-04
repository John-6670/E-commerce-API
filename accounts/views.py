from rest_framework import generics, viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from .models import Address
from .serializers import UserSerializer, AddressSerializer
from .utils import generate_email_verification_token, verify_email_token

User = get_user_model()


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.request.user
        old_email = user.email
        new_email = self.request.data.get('email')

        updated_user = serializer.save()

        if new_email and new_email != old_email:
            updated_user.is_verified = False
            updated_user.save(update_fields=['is_verified'])


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()

    def get_queryset(self):
        return self.request.user.addresses.all()


class EmailVerificationView(views.APIView):
    def get(self, request, token):
        payload = verify_email_token(token)
        if not payload:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = payload.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()
        return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)


class SendVerificationEmailView(views.APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        if not user.email:
            return Response({'error': 'No email associated with this account.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_verified:
            return Response({'error': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate token and build the verification URL.
        token = generate_email_verification_token(user)
        verification_url = request.build_absolute_uri(
            reverse('email-verify', kwargs={'token': token})
        )

        subject = 'Verify Your Email'
        message = f'Hi {user.username},\n\nClick the link below to verify your email:\n{verification_url}'

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        return Response({'message': 'Verification email sent.'}, status=status.HTTP_200_OK)
