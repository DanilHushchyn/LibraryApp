from django.http import HttpResponseForbidden
from multiselectfield import MultiSelectField as MSField
from django.contrib.auth.mixins import AccessMixin
from functools import wraps
from django.db.models import QuerySet
from django.db import models
from rest_framework.response import Response

from config import settings


class MultiSelectField(MSField):
    """Custom Implementation of MultiSelectField
    to achieve Django 5.0 compatibility

    See:
    https://github.com/goinnn/django-multiselectfield/issues/141#issuecomment-1911731471
    """

    def _get_flatchoices(self):
        """Some method for adapting MultiselectField to Django 5.0+
        :return:
        """
        flat_choices = super(models.CharField, self).flatchoices

        class MSFFlatchoices(list):
            # Used to trick django.contrib.admin.utils.display_for_field
            # into not treating the list of values as a
            # dictionary key (which errors out)
            def __bool__(self):
                return False

            __nonzero__ = __bool__

        return MSFFlatchoices(flat_choices)

    flatchoices = property(_get_flatchoices)


class VisitorRequiredMixin(AccessMixin):
    """Verify that the current user is librarian."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'visitor'):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class LibrarianRequiredMixin(AccessMixin):
    """Verify that the current user is librarian."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'librarian'):
            return HttpResponseForbidden()
            # return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
