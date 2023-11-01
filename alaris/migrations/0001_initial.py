# Generated by Django 4.2.5 on 2023-11-01 08:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_carrier_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=120)),
                ('is_active', models.BooleanField()),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_product_type_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=120)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_product_id', models.PositiveIntegerField(unique=True)),
                ('account_currency_code', models.CharField(max_length=10)),
                ('external_account_id', models.PositiveIntegerField()),
                ('is_active', models.BooleanField()),
                ('caption', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=60)),
                ('direction', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('notes', models.CharField(blank=True, max_length=120)),
                ('insert_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='alaris.carrier', to_field='external_carrier_id')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='alaris.producttype', to_field='external_product_type_id')),
            ],
        ),
    ]
