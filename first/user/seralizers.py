from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Пароль не будет возвращаться в ответах API
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}  # Для удобства ввода в API интерфейсе
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'view', 'name_firma', 'inn', 'kPP',
            'Address', 'email', 'director', 'password'
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
        # Хешируем пароль перед сохранением
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
