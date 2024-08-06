from django.utils import timezone
from rest_framework import serializers

from src.core.models import Book, Author, VisitorDebt


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['fullname']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance: Book):
        representation = super().to_representation(instance)
        representation['genres'] = instance.get_genres_display()
        return representation


class MyBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(required=False)

    class Meta:
        model = VisitorDebt
        fields = [
            'book',
            'date_took'
        ]

    def to_representation(self, instance: VisitorDebt):
        representation = super().to_representation(instance)
        diff = timezone.now().date() - instance.date_took
        count_days = 0 if diff.days < 0 else diff.days
        representation['count_days'] = count_days
        return representation
