from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
        Базовый пользователь
    """
    email = models.EmailField(unique=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.last_name + " " + self.first_name

    class Meta(AbstractUser.Meta):
        db_table = 'custom_users'
        ordering = ['-date_joined']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Visitor(models.Model):
    """
        Решения для роли Посетитель
    """
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='visitor')
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name

    class Meta:
        db_table = 'visitors'
        ordering = ['-user__date_joined']
        verbose_name = "Visitor"
        verbose_name_plural = "Visitors"


class Librarian(models.Model):
    """
        Решения для роли библиотекарь
    """
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='librarian')
    staff_number = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.user.last_name + " " + self.user.first_name

    class Meta:
        db_table = 'librarians'
        ordering = ['-user__date_joined']
        verbose_name = "Librarian"
        verbose_name_plural = "Librarians"
