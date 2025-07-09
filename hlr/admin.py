import csv

from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.http.response import HttpResponse
import pandas as pd

from hlr.models import Task, TaskDetail, HlrProduct
from hlr.forms import TaskCreateForm
from hlr.tasks import celery_task_handler


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status',
        'author',
        'insert_time',
        'last_update_time',
        'task_details_link',
    ]

    # ⬇️ Убираем стандартный рендер всех полей
    fieldsets = [(None, {'fields': []})]

    # ⬇️ Подключаем свой шаблон формы
    change_form_template = 'admin/hlr/task/change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        """
        Use custom form only when creating a new Task
        """
        if obj is None:
            kwargs['form'] = TaskCreateForm
        return super().get_form(request, obj, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == "POST":
            form_class = self.get_form(request)
            form = form_class(request.POST, request.FILES)

            # Вызовем ручной is_valid(), чтобы сработал clean()
            if not form.is_valid() and hasattr(form, '_custom_errors'):
                for msg in form._custom_errors:
                    self.message_user(request, msg, level=messages.ERROR)

        return super().add_view(request, form_url, extra_context)

    def save_model(self, request, obj: Task, form, change):
        msisdns = []
        msisdn_field = form.cleaned_data['msisdn']
        upload_file = form.cleaned_data['file']

        if not msisdn_field and not upload_file:
            self.message_user(request, "Fill msisdn or load file", level=messages.SUCCESS)

        hlrs = list(form.cleaned_data['hlr'].values_list('product_id', flat=True))
        mnps = list(form.cleaned_data['mnp'].values_list('product_id', flat=True))

        if not hlrs and not mnps:
            self.message_user(request, "Choose MNP or HLR provider", level=messages.SUCCESS)

        hlrs_external_id = hlrs + mnps

        if upload_file:
            file_name = upload_file.name.lower()
            try:
                # Определяем формат
                if file_name.endswith('.csv'):
                    df = pd.read_csv(upload_file, encoding='utf-8-sig')
                elif file_name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(upload_file)
                else:
                    raise ValueError("Unsupported file format")

                # Определяем нужную колонку
                if df.shape[1] == 1:
                    column_data = df.iloc[:, 0]
                else:
                    # ищем колонку с названием "Destination number" без учёта регистра
                    destination_col = next((col for col in df.columns if col.strip().lower() == 'destination number'),
                                           None)
                    print(destination_col)
                    if destination_col:
                        column_data = df[destination_col]
                    else:
                        raise ValueError("Destination number column not found in uploaded file")

                msisdn_from_file = column_data.dropna().astype(str).map(str.strip).map(lambda x: x.lstrip('\ufeff'))
                msisdns.extend(msisdn_from_file.tolist())

            except Exception as e:
                # Обработка ошибок, если нужно вывести пользователю — можно логгировать или кидать ValidationError
                print(f"Error processing uploaded file: {e}")

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
        'message',
    ]

    readonly_fields = ['author']
    # list_filter = ['task__author__username',]
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
