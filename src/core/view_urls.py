"""
URL configuration for app core.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from src.core.views import BooksListView, DebtorsListView, TakeBookView, MyBooksListView, ReturnBookView

urlpatterns = [
    path('books/', BooksListView.as_view(), name='books'),
    path('my-books/', MyBooksListView.as_view(), name='my_books'),
    path('books/take/<str:pk>', TakeBookView.as_view(), name='take_book'),
    path('books/return/<str:pk>', ReturnBookView.as_view(), name='return_book'),
    path('debtors/', DebtorsListView.as_view(), name='debtors'),
]
