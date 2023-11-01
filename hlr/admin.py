from django.contrib import admin

from hlr.models import Task, TaskDetail, HlrProduct
from hlr.forms import TaskCreateForm
from hlr.tasks import celery_task_handler


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin[Task]):
    list_display = [
        'id',
        'status',
        'author',
        'insert_time',
        'last_update_time',

    ]

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = TaskCreateForm

        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj: Task, form, change):
        msisdn = form.cleaned_data['msisdn'].split(',')
        form.instance.author = request.user
        super(TaskAdmin, self).save_model(request, obj, form, change)
        celery_task_handler(task=obj,
                            msisdns=msisdn,
                            hlr_products_external_id=form.cleaned_data['hlr'],
                            )


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
