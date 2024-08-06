from django.db.models import Case, When, Value, BooleanField
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.generic import ListView, View

from src.core.models import Book, VisitorDebt
from src.core.utils import LibrarianRequiredMixin, VisitorRequiredMixin
from src.users.models import CustomUser, Visitor


class BooksListView(VisitorRequiredMixin, ListView):
    """
       Created to display all books
    """
    template_name = 'core/books.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        visitor: Visitor = self.request.user.visitor
        user_book_ids = [debt.book_id for debt in visitor.debts.all()]
        books = Book.objects.prefetch_related('author').all().annotate(
            taken=Case(
                When(id__in=user_book_ids, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        return books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Book.objects.count()
        return context


class MyBooksListView(VisitorRequiredMixin, ListView):
    """
       Created to display all current user's books
    """
    template_name = 'core/my_books.html'
    model = Book
    context_object_name = 'my_books'
    paginate_by = 10

    def get_queryset(self):
        visitor: Visitor = self.request.user.visitor
        my_books = (VisitorDebt.objects
                    .select_related('book')
                    .filter(visitor=visitor))
        for my_book in my_books:
            diff = timezone.now().date() - my_book.date_took
            count_days = 0 if diff.days < 0 else diff.days
            my_book.count_days = count_days
        return my_books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        visitor: Visitor = self.request.user.visitor
        count = VisitorDebt.objects.filter(visitor=visitor).count()
        context['count'] = count
        return context


class DebtorsListView(LibrarianRequiredMixin, ListView):
    """
       Created to display all users(debtors)
    """
    template_name = 'core/debtors.html'
    model = CustomUser
    context_object_name = 'debtors_books'
    paginate_by = 10

    def get_queryset(self):
        debtors_books = (VisitorDebt.objects
                         .select_related('book', 'visitor__user')
                         .order_by('visitor__user__username'))
        for debtor_book in debtors_books:
            today = timezone.now()
            date_took = debtor_book.date_took
            current_days_passed = (today.date() - date_took).days
            if current_days_passed < 0:
                current_days_passed = 0
            debtor_book.current_days_passed = current_days_passed
        return debtors_books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        count = VisitorDebt.objects.count()
        context['count'] = count
        return context


class TakeBookView(VisitorRequiredMixin, View):
    """
       Created to take book by user for random period
    """

    def post(self, request: HttpRequest, *args, **kwargs):
        book_id = self.kwargs['pk']
        visitor: Visitor = request.user.visitor
        data = {}
        if visitor.debts.filter(book_id=book_id).exists():
            data['message'] = 'Книга уже была взята ранее.'
            return JsonResponse(data, status=409)
        else:
            VisitorDebt.objects.create(
                visitor=visitor,
                book_id=book_id,
            )
            msg = 'Книга успешно взята и добавлена в мои книги.'
            data['message'] = msg
            return JsonResponse(data, status=200)


class ReturnBookView(VisitorRequiredMixin, View):
    """
       Created to return book to library by user
    """

    def post(self, request: HttpRequest, *args, **kwargs):
        book_id = self.kwargs['pk']
        visitor: Visitor = request.user.visitor
        data = {}
        try:
            visitor_book = visitor.debts.get(book_id=book_id)
        except VisitorDebt.DoesNotExist:
            data['message'] = 'Вы не брали эту книгу в библиотеке.'
            return JsonResponse(data, status=404)
        visitor_book.delete()
        msg = 'Книга возвращена библиотеке.'
        data['message'] = msg
        return JsonResponse(data, status=200)
