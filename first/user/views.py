from venv import logger

from django.core.serializers import serialize
from django.shortcuts import render
from .models import CustomUser
from .seralizers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class RegisterView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        try:
            if not serializer.is_valid():
                logger.error(f'Ошибка формы {serialize.errors}')
                return Response(
                    {
                        "error": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user = serializer.save()
                return Response({
                    'user': user
                }, status=status.HTTP_201_CREATED
                )

        except Exception as e:
            logger.error(f'Ошибка создании профиля: {str(e)}', exc_info=True)
            return Response(
                {
                    "error" :"profile create failed"
                },
                status =status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, create = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token":token.key,
                'user': user.pk,
                'email': user.email
            },
            status=status.HTTP_200_OK
        )

