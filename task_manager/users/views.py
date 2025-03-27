from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UsersForm
from .models import Users
from django.contrib import messages
from django.shortcuts import redirect


class SignUp(SuccessMessageMixin, CreateView):
    form_class = UsersForm
    success_url = reverse_lazy("login")
    template_name = "users/registration.html"
    extra_context = {'title': _('Create user')}
    success_message = _('User created successfully')


class ListUsers(ListView):
    model = Users
    context_object_name = 'users'
    extra_context = {'title': _('Users')}


# Правила для Update and Delete, установленные так, что изменять и удалять
# данные пользователя, может только сам пользователь
class RulesMixin:

    # Убедимся, что текущий пользователь имеет разрешение.
    def has_permission(self) -> bool:
        return self.get_object().pk == self.request.user.pk

    # Диспетчер отвечающий за статус аутентификации и вывод ответа
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                messages.error(self.request, _('You are not authorized!'))
            )
            return redirect('login')

        elif not self.has_permission():
            messages.error(
                request,
                messages.error(self.request, _("You have't permission!"))
            )
            return redirect('home_users')
        return super().dispatch(request, *args, **kwargs)


class UpdateUser(RulesMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UsersForm
    success_url = reverse_lazy('home_users')
    success_message = _('User successfully changed')


class DeleteUser(RulesMixin, SuccessMessageMixin, DeleteView):
    model = Users
    success_url = reverse_lazy('home_users')
    success_message = _('User successfully deleted')
