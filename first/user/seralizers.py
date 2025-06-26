from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Пароль не будет возвращаться в ответах API
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}  # Для удобства ввода в API интерфейсе
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'view',
            'name_firma', 'inn', 'kPP',
            'Address', 'director'
            # добавьте все необходимые поля
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'inn': {'validators': [
                RegexValidator(
                    regex=r'^\d{10,12}$',
                    message='ИНН должен содержать 10 или 12 цифр'
                )
            ]}
        }

    def create(self, validated_data):
        # Создаем пользователя с хешированным паролем
        user = User.objects.create(
            email=validated_data['email'],
            # Другие обязательные поля
            view=validated_data.get('view'),
            name_firma=validated_data.get('name_firma'),
            inn=validated_data.get('inn'),
            kPP=validated_data.get('kPP'),
            Address=validated_data.get('Address'),
            director=validated_data.get('director'),
            password=make_password(validated_data['password'])
        )
        return user

    def to_representation(self, instance):
        # Определяем какие поля возвращаются при чтении
        representation = super().to_representation(instance)
        # Удаляем пароль (на всякий случай)
        representation.pop('password', None)
        return representation

    def validate_inn(self, value):
        if value and User.objects.filter(inn=value).exists():
            raise serializers.ValidationError("Пользователь с таким ИНН уже существует")
        return value


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['id', 'email', 'view', 'name_firma', 'inn', 'director']