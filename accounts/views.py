from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Address
from .serializers import UserSerializer, AddressSerializer

User = get_user_model()


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()

    def get_queryset(self):
        return self.request.user.addresses.all()
