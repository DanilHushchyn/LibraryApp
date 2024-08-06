from allauth.socialaccount.models import (SocialApp,
                                          SocialToken,
                                          SocialAccount)
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from rest_framework.authtoken.models import TokenProxy
from simple_history.admin import SimpleHistoryAdmin

from src.core.models import Book, Author, VisitorDebt


@admin.register(Book)
class BookAdminClass(SimpleHistoryAdmin):
    """
    Admin configuration for model Book.
    """
    list_display = ['name', "author",
                    ]

    ordering = ["genres"]


@admin.register(Author)
class AuthorAdminClass(ModelAdmin):
    """
    Admin configuration for model Author.
    """
    pass


@admin.register(VisitorDebt)
class VisitorDebtAdminClass(ModelAdmin):
    """
    Admin configuration for model VisitorDebt.
    """
    pass

admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(TokenProxy)
