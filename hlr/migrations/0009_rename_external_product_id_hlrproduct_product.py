# Generated by Django 4.2.5 on 2023-10-24 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hlr', '0008_alter_hlrproduct_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hlrproduct',
            old_name='external_product_id',
            new_name='product',
        ),
    ]
