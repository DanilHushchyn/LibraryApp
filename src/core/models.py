from django.db import models
from simple_history.models import HistoricalRecords

from src.core.utils import MultiSelectField


class Author(models.Model):
    """
    Хранит всех авторов
    """
    fullname = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ["-id"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        db_table = "authors"


class Book(models.Model):
    """
    Хранит все книги в системе
    """
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    GENRES_CHOICES = (
        ('fantasy', 'Фантастика'),
        ('adventure', 'Приключения'),
        ('detective', 'Детектив'),
        ('horror', 'Ужасы'),
        ('thriller', 'Триллер'),
        ('mysticism', 'Мистика'),
        ('action', 'Боевик'),
    )
    genres = MultiSelectField(
        choices=GENRES_CHOICES, min_choices=1, max_length=500
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        db_table = "books"


class VisitorDebt(models.Model):
    """
    Хранит долги читателей библиотеки
    """
    visitor = models.ForeignKey('users.Visitor', on_delete=models.CASCADE,
                                related_name='debts')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_took = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.visitor.user} - {self.book.name}'

    class Meta:
        unique_together = ('book', 'visitor')
        ordering = ['book__name']
        verbose_name = "Долг посетителя"
        verbose_name_plural = "Долги посетителей"
        db_table = "visitor_debts"
