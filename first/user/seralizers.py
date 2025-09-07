from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
        Сериализатор для чтения данных пользователя.
    """

    class Meta:
        model = User
        fields = [
            'id', 'email', 'view', 'name_firma', 'inn',
            'kPP', 'Address', 'director', 'is_active',       #  fields - какие поля включаются:
            'inn', 'kPP', 'Address', 'director',
            'is_staff', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания данных пользователя.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'view', 'name_firma',
            'inn', 'kPP', 'Address', 'director'
        ]

    # ✅ Методы должны быть НА УРОВНЕ КЛАССА, не внутри Meta!
    def validate(self, attrs):
        """
        Проверяет совпадение паролей.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Создает пользователя с хэшированным паролем.
        """
        # Извлекаем и удаляем служебные поля
        password = validated_data.pop('password')
        validated_data.pop('password2')  # Просто удаляем, не используем

        # Создаем пользователя
        user = User.objects.create(**validated_data)

        # Устанавливаем пароль (автоматически хэшируется)
        user.set_password(password)
        user.save()

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'view', 'name_firma', 'inn', 'kPP',
            'Address', 'director', 'is_active'
        ]


