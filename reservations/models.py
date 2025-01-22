from django.core.validators import MaxValueValidator
from django.db import models

from django.conf import settings


NULLABLE = {"blank": True, "null": True}


class Reservation(models.Model):
    STATUS_PENDING = "В ожидании"
    STATUS_CONFIRMED = "Подтвержден"

    STATUS_CHOICES = [
        (STATUS_PENDING, "статус: В ожидании"),
        (STATUS_CONFIRMED, "статус: Подтвержден"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    guests = models.PositiveIntegerField(default='2', validators=[MaxValueValidator(25)], verbose_name="Количество персон", help_text='Введите количество гостей')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя", help_text='Введите ваше имя')
    email = models.EmailField(unique=True, verbose_name="Электронная почта", help_text='Введите вашу электронную почту')
    message = models.TextField(**NULLABLE)
