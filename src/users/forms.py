from django import forms
from django.contrib.auth.forms import AuthenticationForm

from src.users.models import CustomUser


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)  # and add the remember_me field
    role = forms.CharField()  # and add the role field for login to specific page


class RegisterVisitorForm(forms.ModelForm):
    address = forms.CharField(
        label="Домашний адрес",
        strip=False,
        widget=forms.TextInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    repeat_password = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={})
        }


class RegisterLibrarianForm(forms.ModelForm):
    repeat_password = forms.CharField(
        label="Повторите пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={})
        }
