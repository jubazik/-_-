from django.db import models
from first.user.models import CustomUser


class Type(models.Model):
    """
    модель хранит данные о типы  измирения 'шт, кг, и тд'

    """
    pass


"""
    модель хранит данные о товаре 
"""
class Products(models.Model):
    pass


class OrderTable(models.Model):
    """
    модель хранит данные о заказе
    """
    pass


class OrderItem(models.Model):
    """
    модель хранит данные детально о заказе

    """
    pass

# Create your models here.
