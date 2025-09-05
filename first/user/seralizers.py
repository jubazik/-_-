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
        write_only=True,  # Что делает: Поле используется только для записи (ввода), но не возвращается в ответах API.
        required=True,  # Что делает: Поле обязательно для заполнения.
        validators=[validate_password]  # Что делает: Добавляет валидацию сложности пароля.

    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'view', 'name_firma',     # fields - какие поля включаются:
            'inn', 'kPP', 'Address', 'director'
        ]
        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:#Сравнивает значения полей password и password2
                raise serializers.ValidationError({"password": "Password fields didn't match."}) # Вызов ошибки при несовпадении:
            return attrs

        def create(self, validated_data):
            validated_data.pop('password2')
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
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


