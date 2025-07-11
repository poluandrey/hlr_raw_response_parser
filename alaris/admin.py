from datetime import datetime
from io import BytesIO
import json

import pandas as pd
from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect

from .enterprise_api.client import EnterpriseClient
from .enterprise_api.schema import UpdateRecurringFee
from .models import Carrier, Account, AdminTool
from .forms import DownloadForm, UploadForm


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'external_id')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'carrier_external_id', 'currency_code')


@admin.register(AdminTool)
class AdminToolAdmin(admin.ModelAdmin):
    change_list_template = "admin/carrier_account_tool.html"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('', self.admin_site.admin_view(self.carrier_account_view), name="carrier-account-tool"),
        ]
        return custom + urls

    def carrier_account_view(self, request):
        download_form = DownloadForm(request.POST or None, prefix='download')
        upload_form = UploadForm(request.POST or None, request.FILES or None, prefix='upload')

        if request.method == 'POST':
            client = EnterpriseClient(base_url=settings.EAPI_BASE_URL, auth=settings.EAPI_AUTH)
            if 'download-submit' in request.POST and download_form.is_valid():
                carrier = download_form.cleaned_data['carrier']
                account = download_form.cleaned_data['account']
                start_date_lower_bound = download_form.cleaned_data['start_date_lower_bound']
                start_date_upper_bound = download_form.cleaned_data['start_date_upper_bound']
                end_date_lower_bound = download_form.cleaned_data['end_date_lower_bound']
                end_date_upper_bound = download_form.cleaned_data['end_date_upper_bound']

                # client = EnterpriseClient(base_url=settings.EAPI_BASE_URL, auth=settings.EAPI_AUTH)
                recurring_fees = client.recurring_fee.get_all(
                    acc_id=account.external_id,
                    start_date1=start_date_lower_bound,
                    start_date2=start_date_upper_bound,
                    end_date1=end_date_lower_bound,
                    end_date2=end_date_upper_bound,
                )
                records = []
                for recurring_fee in recurring_fees:
                    rates = client.recurring_fee_period.get_period_list(id=recurring_fee.id)
                    if rates:
                        latest = max(rates, key=lambda r: datetime.strptime(r.start_date, "%Y.%m.%d %H:%M:%S"))
                        records.append({
                            'id': recurring_fee.id,
                            'details': recurring_fee.details,
                            'start_date': recurring_fee.start_date,
                            'end_date': recurring_fee.end_date,
                            'rate': latest.rate,
                            'period_start_date': latest.start_date,
                            'volume': latest.volume,
                        })

                df = pd.DataFrame(records)
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Recurring Fees')

                output.seek(0)
                filename = f"recurring_fees_{account.external_id}.xlsx"
                return HttpResponse(
                    output.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={'Content-Disposition': f'attachment; filename="{filename}"'}
                )

            elif 'upload-submit' in request.POST and upload_form.is_valid():
                try:
                    file = request.FILES['upload-file']
                    print(f'file name: {file}')
                    df = pd.read_excel(file)
                    for row in df.to_dict(orient='records'):
                        print(row)
                        period_list = [{
                            "rate": str(row["rate"]),
                            "volume": str(row["volume"]),
                            "period_start_date": row["period_start_date"]
                        }]
                        schema = UpdateRecurringFee(
                            id=row['id'],
                            details=row['details'],
                            start_date=row['start_date'],
                            end_date=row['end_date'],
                            period_list=json.dumps(period_list),
                        )
                        try:
                            client.recurring_fee.update(schema)
                        except Exception as e:
                            print(e)
                    self.message_user(request, "Файл успешно загружен", level=messages.SUCCESS)
                except Exception as e:
                    print(e)
                    self.message_user(request, f"Ошибка при загрузке файла: {e}", level=messages.ERROR)

                return redirect(request.path)

        context = {
            **self.admin_site.each_context(request),
            'download_form': download_form,
            'upload_form': upload_form,
            'title': "Recurring Fee Tool",
        }
        return render(request, "admin/carrier_account_tool.html", context)



