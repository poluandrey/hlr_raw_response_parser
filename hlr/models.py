from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.contrib.postgres.fields import ArrayField
from django_fsm import FSMField, transition

from alaris.models import Product

User = get_user_model()


# TODO also need to check product_type
def validate_alaris_product_id(alaris_product_ids: list[int]) -> None:
    for alaris_product_id in alaris_product_ids:
        if not Product.objects.filter(alaris_product_id=alaris_product_id).exists():
            raise ValidationError(f'{alaris_product_id} not valid HLR product')


class Task(models.Model):
    status = FSMField(default='new')
    author = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='tasks',
    )
    alaris_product_id = ArrayField(
        models.IntegerField(blank=False),
        # default=list,
        validators=[validate_alaris_product_id],
    )
    msisdn = ArrayField(models.CharField(max_length=20, blank=False))
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

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
    alaris_product_id = models.ForeignKey(Product,
                                          on_delete=models.PROTECT,
                                          to_field='alaris_product_id',
                                          related_name='tasks',
                                          )
    msisdn = models.CharField(max_length=20, blank=False)
    result = models.IntegerField()
    mcc = models.CharField(max_length=3, null=True, blank=True)
    mnc = models.CharField(max_length=3, null=True, blank=True)
    ported = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    message = models.CharField(max_length=200, null=True, blank=True)
    http_error_code = models.IntegerField()
