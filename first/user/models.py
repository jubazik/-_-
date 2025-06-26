from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator




class CustomUser(AbstractUser):
    VIEW = [
        ('legal', 'Юрид/лицо'),
        ('IP', 'ИП'),
    ]
    view = models.CharField(max_length=25, choices=VIEW, blank=True, verbose_name='вид')
    name_firma = models.CharField(max_length=150, verbose_name='Наименование', blank=True, null=True),
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

    def __str__(self):
        return f"фирма: {self.email} - директор: {self.director}"
# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Profile')


    def __str__(self):
        return f'{self.user.email}: Profile'