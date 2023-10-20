from django.contrib.auth import get_user_model
from django.db import models
from django_fsm import FSMField, transition

from alaris.models import Product

User = get_user_model()


class Task(models.Model):
    status = FSMField(default='new')
    author = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='tasks',
    )
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-insert_time']

    @transition(field=status, source='new', target='in progress')
    def in_progress(self) -> None:
        pass

    @transition(field=status, source='in progress', target='ready')
    def ready(self) -> None:
        pass

    def __str__(self) -> str:
        return f'task id {self.pk} <{self.author.username}>'


class TaskDetail(models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name='details')
    external_product_id = models.ForeignKey(Product,
                                            on_delete=models.PROTECT,
                                            to_field='external_product_id',
                                            related_name='tasks',
                                            )
    msisdn = models.CharField(max_length=20, blank=False)
    result = models.IntegerField(null=True)
    mccmnc = models.CharField(max_length=6, null=True, blank=True)
    ported = models.CharField(max_length=10)
    message = models.CharField(max_length=200, null=True, blank=True)
    http_error_code = models.IntegerField(null=True)

    def __str__(self):
        return (f'{self.pk} for {self.msisdn} via {self.external_product_id} '
                f'created by {self.task.author}')
