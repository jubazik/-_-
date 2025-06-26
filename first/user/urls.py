from django.urls import path
from .views import CustomAuthToken, RegisterView

urlpatterns =[
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register')
]