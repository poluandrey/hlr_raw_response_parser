from django.contrib import admin

from hlr.models import Task, TaskDetail



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status',
        'author',
        'alaris_product_id',
        'msisdn',
        'insert_time',
        'last_update_time',
    ]


@admin.register(TaskDetail)
class TaskDetailAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'task',
        'alaris_product_id',
        'msisdn',
        'result',
        'mcc',
        'mnc',
        'ported',
        'message',
        'http_error_code',
    ]

