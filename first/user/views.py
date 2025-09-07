from distutils.core import setup_keywords
from xmlrpc.client import Fault

from django.core.serializers import serialize
from django.db.models import Q, Count
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .seralizers import UserSerializer, UserCreateSerializer, UserUpdateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.
    Предоставляет стандартные CRUD операции + кастомные actions.
    """
    queryset = User.objects.all().order_by('-date_joined')
    """Что делает:
User.objects.all() - выбирает ВСЕХ пользователей из базы
.order_by('-date_joined') - сортирует по дате регистрации в обратном порядке (новые первыми)"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Что означает: Аутентифицированные пользователи → могут делать всё (READ/WRITE) Анонимные пользователи → могут только читать (READ ONLY)

    def get_serializer_class(self):
        """
                Выбор сериализатора в зависимости от действия.
        :return:
        """
        if self.action == "create":
            return UserCreateSerializer  # Для создания
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer  # Для обновления
        else:
            return UserSerializer  # Для чтения и остального

    def get_permissions(self):
        """
              Настройка permissions в зависимости от действия.
              """
        if self.action == 'create':
            return [permissions.AllowAny()]  # Регистрация доступна всем
        elif self.action in ['update', 'partial_update', 'destroy']:  # Изменение только для админов или владельцев
            return [permissions.IsAdminUser() & permissions.IsAuthenticated()]
        elif self.action == 'me':
            # Endpoint /me/ только для авторизованных
            return [permissions.IsAuthenticated()]
        elif self.action == 'stats':
            # Статистика только для админов
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        """Фильтрация queryset в зависимости от прав пользователя"""
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        elif user.is_authenticated:
            # Обычный пользователи видят только свой профиль
            return User.objects.filter(id=user.id)
        return User.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
                Кастомный endpoint для получения текущего пользователя.
                GET /api/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_password(self, request, pk=None):
        """
                Кастомный endpoint для смены пароля.
                POST /api/users/{id}/set_password/
        """
        user = self.get_object()
        password = request.data.get("password")
        if password:
            user.set_password(password)
            user.save()
            return Response({'status': "password set"})
        return Response(
            {"Error": "Password not provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def stats(self, request):
        """
              Кастомный endpoint для статистики пользователей.
              GET /api/users/stats/
        """
        from django.db.models import Count
        stats = User.objects.aggregate(
            total_users=Count('id'),
            active_users=Count('id', filter=Q(is_active=True)),
            staff_users=Count('id', filter=Q(is_staff=True))
        )


        return Response(stats)
