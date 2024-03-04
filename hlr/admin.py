import csv

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http.response import HttpResponse

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
        'task_details_link',
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
        msisdns = []
        msisdn_field = form.cleaned_data['msisdn']
        upload_file = form.cleaned_data['file']
        hlrs_external_id = list(form.cleaned_data['hlr'].values_list('product_id', flat=True))

        if upload_file:
            # for chunk in upload_file.chunks():
            #     msisdn_from_file = chunk.decode('utf-8-sig').replace('\n', '').strip().split('\r')
            #     msisdn_from_file = [msisdn.lstrip('\ufeff') for msisdn in msisdn_from_file]
            #     msisdns.extend(filter(lambda msisdn: True if msisdn else False, msisdn_from_file))
            with open(upload_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                msisdn_from_file = [row for row in reader]
                msisdns.extend(filter(lambda msisdn: True if msisdn else False, msisdn_from_file))

        if msisdn_field:
            msisdns.extend(msisdn_field.split(','))

        form.instance.author = request.user
        super().save_model(request, obj, form, change)
        celery_task_handler.delay(task_id=obj.pk,
                                  msisdns=msisdns,
                                  hlr_products_external_id=hlrs_external_id)

    def task_details_link(self, obj):
        url = reverse('admin:hlr_taskdetail_changelist') + f'?task={obj.id}'
        return format_html('<a href="{}">View TaskDetails</a>', url)

    task_details_link.short_description = 'Details'


@admin.register(TaskDetail)
class TaskDetailAdmin(admin.ModelAdmin):
    list_display = [
        'insert_time_formatted',
        'author',
        'status',
        'request_id',
        'product',
        'msisdn',
        'result',
        'mccmnc',
        'ported',
        'presents',
        'roaming',
    ]

    readonly_fields = ['author']
    list_filter = ['task__author__username', 'msisdn']
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        field_names = [
            'insert_time',
            'status',
            'request_id',
            'product',
            'msisdn',
            'result',
            'mccmnc',
            'ported',
            'presents',
            'roaming',
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=task_detail-{queryset[0].task.pk}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for task_detail in queryset:
            writer.writerow([task_detail.insert_time,
                             task_detail.status,
                             task_detail.request_id,
                             task_detail.product.description,
                             task_detail.msisdn,
                             task_detail.result,
                             task_detail.mccmnc,
                             task_detail.ported,
                             task_detail.presents,
                             task_detail.roaming,
                             ],
                            )

        return response

    def author(self, obj):
        return obj.task.author

    def insert_time_formatted(self, obj):
        return obj.insert_time.strftime('%d.%m.%Y %H:%M:%S')

    insert_time_formatted.short_description = 'insert_time'


@admin.register(HlrProduct)
class HlrProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'type',
    ]
