from django.db import models
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users
from task_manager.labels.models import Labels
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Tasks(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Task name'))
    description = models.TextField(max_length=500, blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_('Status')
    )
    author = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author'),
    )
    executor = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Executor'),
    )
    labels = models.ManyToManyField(
        Labels,
        related_name='label',
        through='TaskRelationLabel',
        blank=True,
        verbose_name=_('Label')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("=Task=")
        verbose_name_plural = _("=Tasks=")


class TaskRelationLabel(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)
