from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ProductType(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Carrier(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    is_active = models.BooleanField()
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    currency_code = models.CharField(max_length=10)
    carrier_external_id = models.ForeignKey(
        Carrier,
        to_field='external_id',  # 👈 связываемся по external_id
        on_delete=models.PROTECT,
        related_name='accounts'
    )


class Product(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    account_currency_code = models.CharField(max_length=10)
    external_account_id = models.PositiveIntegerField()
    carrier = models.ForeignKey(
        Carrier,
        on_delete=models.PROTECT,
        related_name='products',
    )
    is_active = models.BooleanField()
    caption = models.CharField(max_length=150)
    description = models.CharField(max_length=60)
    direction = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )
    notes = models.CharField(max_length=120, blank=True, null=True)
    type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name='products',
    )
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
        # return f'{self.caption} <{self.type.name}>'


class AdminTool(models.Model):
    class Meta:
        app_label = 'alaris'
        managed = False
        verbose_name = 'recurring fee tool'
        verbose_name_plural = 'recurring fee tool'
        default_permissions = ()


    def __str__(self):
        return "AdminTool"
