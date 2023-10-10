from django.contrib import admin

from alaris.models import Carrier, Product, ProductType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'alaris_product_id',
        'acc_currency_code',
        'alaris_acc_id',
        'carrier',
        'is_active',
        'product_caption',
        'product_direction',
        'product_notes',
        'product_type',
        'insert_time',
        'last_update_time',
    ]


@admin.register(ProductType)
class ProductType(admin.ModelAdmin):
    list_display = [
        'id',
        'alaris_product_type_id',
        'type_name',
        'insert_time',
        'last_update_time',
    ]


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'alaris_car_id',
        'car_name',
        'car_is_active',
        'insert_time',
        'last_update_time',
    ]
