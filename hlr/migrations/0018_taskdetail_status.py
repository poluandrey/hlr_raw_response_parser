# Generated by Django 4.2.5 on 2023-10-27 08:36

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('hlr', '0017_taskdetail_request_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdetail',
            name='status',
            field=django_fsm.FSMField(default='new', max_length=50),
        ),
    ]