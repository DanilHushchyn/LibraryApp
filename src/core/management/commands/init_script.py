# -*- coding: utf-8 -*-
import os
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from src.core.models import Author, Book
from src.users.models import Visitor, Librarian

User = get_user_model()


class Command(BaseCommand):
    _fake_ru = Faker("ru_RU")

    def handle(self, null=None, *args, **options):
        self._create_superuser()
        self._create_librarians()
        self._create_visitor()
        self._create_authors()
        self._create_books()

    @classmethod
    def _create_superuser(cls):
        if not User.objects.exists():
            user = User.objects.create(
                first_name="Данил",
                last_name="Гущин",
                username="admin",
                email="admin@admin.com",
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )
            user.set_password("sword123")
            user.save()

    @classmethod
    def _create_librarians(cls):
        if not Librarian.objects.exists():
            users = []
            for i in range(5):
                while True:
                    username = cls._fake_ru.user_name()
                    if not User.objects.filter(username=username).exists():
                        break
                if i == 0:
                    username = 'librarian'
                while True:
                    email = cls._fake_ru.email()
                    if not User.objects.filter(email=email).exists():
                        break
                user = User(
                    first_name=cls._fake_ru.first_name_male(),
                    last_name=cls._fake_ru.last_name_male(),
                    email=email,
                    username=username,
                )
                user.set_password("sword123")
                users.append(user)
            users = User.objects.bulk_create(users)
            librarians = []
            for user in users:
                while True:
                    staff_number = cls._fake_ru.bothify(text='????-########',
                                                        letters='ABCDE')
                    if not Librarian.objects.filter(staff_number=staff_number).exists():
                        break
                librarian = Librarian(
                    user=user,
                    staff_number=staff_number,
                )
                librarians.append(librarian)
            Librarian.objects.bulk_create(librarians)

    @classmethod
    def _create_visitor(cls):
        if not Visitor.objects.exists():
            users = []
            for i in range(5):
                while True:
                    username = cls._fake_ru.user_name()
                    if not User.objects.filter(username=username).exists():
                        break
                if i == 0:
                    username = 'visitor'
                while True:
                    email = cls._fake_ru.email()
                    if not User.objects.filter(email=email).exists():
                        break
                user = User(
                    first_name=cls._fake_ru.first_name_male(),
                    last_name=cls._fake_ru.last_name_male(),
                    email=email,
                    username=username,
                )
                user.set_password("sword123")
                users.append(user)
            users = User.objects.bulk_create(users)
            visitors = []
            for user in users:
                visitor = Visitor(
                    user=user,
                    address=cls._fake_ru.address(),
                )
                visitors.append(visitor)
            Visitor.objects.bulk_create(visitors)

    @classmethod
    def _create_authors(cls):
        if not Author.objects.exists():
            authors = []
            for i in range(20):
                while True:
                    fullname = cls._fake_ru.name()
                    if not Author.objects.filter(fullname=fullname).exists():
                        break
                author = Author(
                    fullname=fullname,
                )
                authors.append(author)
            Author.objects.bulk_create(authors)

    @classmethod
    def _create_books(cls):
        if not Book.objects.exists():
            author_ids = list(Author.objects.values_list('id', flat=True))
            for i in range(50):
                genre_keys = [key for key, _ in Book.GENRES_CHOICES]
                genres = random.sample(genre_keys, 2)
                Book.objects.create(
                    name=f"Книга {i}",
                    genres=genres,
                    author_id=random.choice(author_ids)
                )

    @classmethod
    def generate_staff_number(cls):
        return cls._fake_ru.bothify(text='????-########',
                                    letters='ABCDE')
