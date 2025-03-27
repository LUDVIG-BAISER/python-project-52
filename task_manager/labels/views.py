from .models import Labels
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
# Create your views here.


# Класс который содержит все общие атрибуты классов CRUD
class LabelsMixin(LoginRequiredMixin, SuccessMessageMixin):
    model = Labels
    extra_context = {'title': _('Labels'), 'button': _('Create')}
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home_labels')
    fields = ['name']


class ListLabels(LabelsMixin, ListView):
    context_object_name = 'labels'


class CreateLabel(LabelsMixin, CreateView):
    success_message = _("Label created successfully")
    template_name = 'apps/apps_form.html'


class UpdateLabel(LabelsMixin, UpdateView):
    success_message = _('Label successfully changed')
    template_name = 'apps/apps_form.html'
    extra_context = {'title': _('Labels'), 'button': _('Change')}


class DeleteLabel(LabelsMixin, DeleteView):
    template_name = 'apps/apps_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(
                self.request,
                _('Label successfully deleted')
            )
            return redirect(reverse_lazy('home_labels'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Error! Can't delete, label in use")
            )
            return redirect(reverse_lazy('home_labels'))
