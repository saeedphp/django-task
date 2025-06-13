from django import forms
from rest_framework import serializers

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=11)
    password = serializers.CharField(required=True)

class UserVerifySerializer(serializers.Serializer):
    code = serializers.CharField(required=True)