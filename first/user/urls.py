from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]
