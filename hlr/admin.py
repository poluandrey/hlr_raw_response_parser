from django.contrib import admin

from hlr.models import Task, TaskDetail


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status',
        'author',
        'external_product_id',
        'msisdn',
        'insert_time',
        'last_update_time',
    ]


@admin.register(TaskDetail)
class TaskDetailAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'task',
        'external_product_id',
        'msisdn',
        'result',
        'mccmnc',
        'ported',
        'message',
        'http_error_code',
    ]
