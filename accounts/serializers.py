from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Address

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'national_id', 'is_seller']
        read_only_fields = ['id']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'country', 'city', 'street_address', 'apartment_address', 'postal_code', 'default', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        address = Address.objects.create(user=self.context['request'].user, **validated_data)
        return address
