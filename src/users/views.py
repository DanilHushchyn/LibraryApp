from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView

from src.core.management.commands.init_script import Command
from src.users.forms import LoginForm, RegisterLibrarianForm, RegisterVisitorForm
from src.users.models import CustomUser, Librarian, Visitor


# Create your views here.
class LoginView(View):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'librarian'):
                return redirect('debtors')
            if hasattr(user, 'visitor'):
                return redirect('books')
        form = self.form_class()
        message = ''
        return render(request, self.template_name,
                      context={'form': form,
                               'message': message})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user: CustomUser = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                if form.cleaned_data['remember_me']:
                    self.request.session.set_expiry(0)
                if role == 'visitor' and hasattr(user, 'visitor'):
                    return redirect('books')
                if role == 'librarian' and hasattr(user, 'librarian'):
                    return redirect('debtors')
        msg = ('Неправильно указан username или пароль, '
               'или у вас нету прав.')
        messages.error(request, msg)
        return render(request, self.template_name, context={'form': form})


class RegisterVisitorView(CreateView):
    template_name = 'users/register_visitor.html'
    form_class = RegisterVisitorForm
    success_url = reverse_lazy('login')

    def post(self, request):
        form = self.form_class(data=request.POST)
        print(111)
        print(form.errors)
        if form.is_valid():
            print(111)

            user = form.save(commit=False)
            user.is_active = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            Visitor.objects.create(
                user=user,
                address=form.cleaned_data['address']
            )
            msg = 'Пользователь успешно создан. Теперь войдите'
            messages.success(request, msg)
            return redirect('login')
        return render(request, self.template_name, context={'form': form})


class RegisterLibrarianView(CreateView):
    template_name = 'users/register_librarian.html'
    form_class = RegisterLibrarianForm
    success_url = reverse_lazy('login')

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.set_password(form.cleaned_data['password'])
            user.save()
            Librarian.objects.create(
                user=user,
                staff_number=Command.generate_staff_number()
            )
            msg = 'Пользователь успешно создан. Теперь войдите'
            messages.success(request, msg)
            return redirect('login')

        return render(request, self.template_name, context={'form': form})
