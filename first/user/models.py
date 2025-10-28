from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле «Электронная почта» должно быть заполнено.")
        email = self.normalize_email(email)
        user = self.model(email=email **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True )
        if extra_fields.get('is_staff') is not True:
            return ValueError("«У суперпользователя должен быть параметр is_staff=True».")
        if extra_fields.get('is_superuser') is not True:
            return ValueError('Суперпользователь должен иметь is_superuser=True.')

class CustomUser(AbstractUser):
    VIEW = [
        ('legal', 'Юрид/лицо'),
        ('IP', 'ИП'),
    ]
    view = models.CharField(max_length=25, choices=VIEW, blank=True, verbose_name='вид')
    name_firma = models.CharField(max_length=150, verbose_name='Наименование', blank=True, null=True)
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,  # Максимум 12 символов для физлиц/ИП
        blank=True,
        null=True,
        unique=True,  # Гарантирует уникальность
        validators=[
            RegexValidator(
                regex=r'^\d{10,12}$',  # 10 или 12 цифр
                message='ИНН должен содержать 10 или 12 цифр'
            )
        ]
    )
    kPP = models.IntegerField(verbose_name='КПП', blank=True,null=True)
    Address = models.CharField(max_length=150, blank=True, verbose_name="Адрес")
    email = models.EmailField(verbose_name='mail',unique=True)
    director = models.CharField(verbose_name='ФИО', blank=True, max_length=50)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"фирма: {self.email} - директор: {self.director}"



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Profile')


    def __str__(self):
        return f'{self.user.email}: Profile'

