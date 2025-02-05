from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'national_id', 'is_seller']
        read_only_fields = ['id']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.addresses.model
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
