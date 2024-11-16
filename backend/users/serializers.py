import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "full_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = str(uuid.uuid4())

        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "full_name")


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")
