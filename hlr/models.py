from django.contrib.auth import get_user_model
from django.db import models
from django_fsm import FSMField, transition

User = get_user_model()


class Task(models.Model):
    status = FSMField(default='new')
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks',
    )
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    @transition(field=status, source='new', target='in progress')
    def in_progress(self):
        pass

    @transition(field=status, source='in progress', target='ready')
    def ready(self):
        pass

    def __str__(self):
        return f'task id {self.pk} <{self.author.username}>'
