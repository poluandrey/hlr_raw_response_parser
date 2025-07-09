from django.http import JsonResponse
from alaris.models import Account

def get_accounts_by_carrier(request):
    carrier_id = request.GET.get('carrier_id')
    accounts = Account.objects.filter(
        carrier_external_id__external_id=carrier_id
    ).values('id', 'external_id', 'currency_code')

    return JsonResponse(list(accounts), safe=False)
