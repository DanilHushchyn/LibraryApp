from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.models import Group

from src.users.models import Librarian, Visitor, CustomUser


class CustomUserForm(forms.ModelForm):
    """
    ModelForm configuration for model MenuItem.
    for admin panel class MenuItemAdminClass
    """

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username',
                  'is_superuser', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
            In this method, I exclude the possibility of the
            Current element choosing itself as a Parent element
        """
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            # pq = (self.fields["parent"].queryset
            #       .exclude(id=instance.pk))
            # self.fields["parent"].queryset = pq

            self.fields["password"].disabled = True


class LibrarianInline(TabularInline):
    """
    Admin configuration for model Librarian.
    """
    model = Librarian


class VisitorInline(TabularInline):
    """
    Admin configuration for model LibraryVisitor.
    """
    model = Visitor


@admin.register(CustomUser)
class CustomUserAdminClass(ModelAdmin):
    """
    Admin configuration for model CustomUser.
    """
    list_display = ['username', "first_name",
                    "last_name", 'is_superuser',
                    'is_librarian', 'is_visitor','has_debts',
                    ]

    @admin.display(
        boolean=True,
        description='Библиотекарь (Librarian)',
    )
    def is_librarian(self, obj: CustomUser):
        if hasattr(obj, 'librarian'):
            return True
        return False

    @admin.display(
        boolean=True,
        description='Читатель (Visitor)',
    )
    def is_visitor(self, obj: CustomUser):
        if hasattr(obj, 'visitor'):
            return True
        return False

    @admin.display(
        boolean=True,
        description='Есть долги',
    )
    def has_debts(self, obj: CustomUser):
        if obj.visitor.debts.count() > 0:
            return True
        return False
    inlines = [
        VisitorInline, LibrarianInline
    ]
    form = CustomUserForm


admin.site.unregister(Group)
