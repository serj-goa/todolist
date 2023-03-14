from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated

from core.models import CustomUser


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('Passwords must match')

        return attrs

    def create(self, validated_data: dict) -> CustomUser:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def create(self, validated_data: dict) -> CustomUser:
        if not (user := authenticate(
            username=validated_data['username'],
            password=validated_data['password'],
        )):
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate(self, attrs: dict):
        if not (user := attrs['user']):
            raise NotAuthenticated

        if not user.check_password(attrs['old_password']):
            raise ValidationError({'old_password': 'field is incorrect'})

        return attrs

    def create(self, validated_data: dict) -> CustomUser:
        raise NotImplementedError

    def update(self, instance: CustomUser, validated_data: dict) -> CustomUser:
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=('password', ))

        return instance
