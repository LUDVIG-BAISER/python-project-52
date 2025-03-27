from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Statuses
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
# Create your views here.


# Класс который содержит все общие атрибуты классов CRUD
class StatusMixin(LoginRequiredMixin, SuccessMessageMixin):
    model = Statuses
    extra_context = {'title': _('Statuses'), 'button': _('Create')}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home_statuses')
    fields = ['name']


class ListStatuses(StatusMixin, ListView):
    context_object_name = 'statuses'


class CreateStatus(StatusMixin, CreateView):
    success_message = _("Status created successfully")
    template_name = 'apps/apps_form.html'


class UpdateStatus(StatusMixin, UpdateView):
    success_message = _('Status successfully changed')
    template_name = 'apps/apps_form.html'
    extra_context = {'title': _('Statuses'), 'button': _('Change')}


class DeleteStatus(StatusMixin, DeleteView):
    template_name = 'apps/apps_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(
                self.request,
                _('Status successfully deleted')
            )
            return redirect(reverse_lazy('home_statuses'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Error! Can't delete, status in use")
            )
            return redirect(reverse_lazy('home_statuses'))
