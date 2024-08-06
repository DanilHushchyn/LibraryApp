from rest_framework.permissions import BasePermission


class IsVisitor(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = 'Доступно только пользователям (Посетитель).'

    def has_permission(self, request, view):
        return bool(hasattr(request.user, 'visitor'))
