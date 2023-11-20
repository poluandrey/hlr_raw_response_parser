from django.contrib import admin

from alaris.models import Carrier, Product, ProductType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'external_id',
        'account_currency_code',
        'external_account_id',
        'carrier',
        'is_active',
        'caption',
        'direction',
        'notes',
        'type',
        'insert_time',
        'last_update_time',
    ]


@admin.register(ProductType)
class ProductType(admin.ModelAdmin):
    list_display = [
        'id',
        'external_id',
        'name',
        'insert_time',
        'last_update_time',
    ]


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'external_id',
        'name',
        'is_active',
        'insert_time',
        'last_update_time',
    ]
