from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator


class ProductType(models.Model):
    alaris_product_type_id = models.PositiveIntegerField()
    type_name = models.CharField(max_length=120)
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type_name


class Carrier(models.Model):
    alaris_car_id = models.PositiveIntegerField()
    car_name = models.CharField(max_length=120)
    car_is_active = models.IntegerField(validators=[MinLengthValidator(0), MaxLengthValidator(1)])
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.car_name


class Product(models.Model):
    alaris_product_id = models.PositiveIntegerField()
    acc_currency_code = models.CharField(max_length=10)
    alaris_acc_id = models.PositiveIntegerField()
    carrier = models.ForeignKey(
        Carrier,
        on_delete=models.PROTECT,
        related_name='products',
    )
    is_active = models.IntegerField(validators=[MinLengthValidator(0), MaxLengthValidator(1)])
    product_caption = models.CharField(max_length=150)
    product_description = models.CharField(max_length=60)
    product_direction = models.IntegerField(validators=[MinLengthValidator(0), MaxLengthValidator(1)])
    product_notes = models.CharField(max_length=120, blank=True)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name='products',
    )
    insert_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product_caption} <{self.product_type.type_name}>'
