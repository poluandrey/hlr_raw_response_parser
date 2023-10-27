from django.contrib import admin

from hlr.models import Task, TaskDetail, HlrProduct


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin[Task]):
    list_display = [
        'id',
        'status',
        'author',
        'insert_time',
        'last_update_time',
    ]


@admin.register(TaskDetail)
class TaskDetailAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'task',
        'status',
        'request_id',
        'external_product_id',
        'msisdn',
        'result',
        'mccmnc',
        'ported',
        'presents',
        'roaming',
        'message',
        'http_error_code',
    ]


@admin.register(HlrProduct)
class HlrProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'type',
    ]
