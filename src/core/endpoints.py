from django.db import IntegrityError
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from src.core.models import Book, VisitorDebt
from src.core.permissions import IsVisitor
from src.core.serializers import BookSerializer, MyBookSerializer


@extend_schema(tags=['books'])
class BookViewSet(PsqMixin, mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = None
    http_method_names = ['get', 'post', 'delete']
    queryset = Book.objects.select_related('author').all()

    psq_rules = {
        ('list', 'my_books', 'take_book', 'return_book'):
            [Rule([IsVisitor], BookSerializer), ],
    }

    @extend_schema(description='Permissions: IsVisitor.\n'
                               "Get all my books.")
    @action(methods=['get'], detail=False)
    def my_books(self, request, *args, **kwargs):
        visitor = request.user.visitor
        user_books = (VisitorDebt.objects
                      .select_related('book__author')
                      .filter(visitor=visitor))
        serializer = MyBookSerializer(user_books, many=True)
        return Response(serializer.data)

    @extend_schema(description='Permissions: IsVisitor.\n'
                               "Get all my books.")
    @action(methods=['post'], url_path='take', detail=True)
    def take_book(self, request, *args, **kwargs):
        data = {}
        try:
            VisitorDebt.objects.create(visitor=request.user.visitor,
                                       book=self.get_object())
        except IntegrityError:
            data['message'] = "Эта книга у вас уже на руках"
            return Response(data, status=409)
        data['message'] = "Книга успешно взята"
        return Response(data)

    @extend_schema(description='Permissions: IsVisitor.\n'
                               "Delete.")
    @action(methods=['delete'], url_path='return', detail=True)
    def return_book(self, request, *args, **kwargs):
        data = {}
        try:
            (VisitorDebt.objects.get(visitor=request.user.visitor,
                                     book=self.get_object())
             .delete())
        except VisitorDebt.DoesNotExist:
            data['message'] = "Эта книга не числится вашим долгом библиотеке."
            return Response(data, status=404)
        data['message'] = "Книга успешно возвращена"
        return Response(data)
