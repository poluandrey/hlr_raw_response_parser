from django import forms
from alaris.models import Carrier, Account


class DownloadForm(forms.Form):
    carrier = forms.ModelChoiceField(
        queryset=Carrier.objects.all().order_by('name'),
        label="Carrier",
        required=True,
        to_field_name='external_id'
    )
    account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        label="Account",
        required=True
    )
    start_date_lower_bound = forms.DateField(
        label="Start Date lower bound", required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    start_date_upper_bound = forms.DateField(
        label="Start Date upper bound", required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date_lower_bound = forms.DateField(
        label="End Date lower bound", required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date_upper_bound = forms.DateField(
        label="End Date upper bound", required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        carrier_id = None
        carrier_field_name = f'{self.prefix}-carrier' if self.prefix else 'carrier'
        carrier_val = self.data.get(carrier_field_name)

        if carrier_val:
            try:
                carrier_id = int(carrier_val)
                self.fields['account'].queryset = Account.objects.filter(
                    carrier_external_id__external_id=carrier_id
                )
            except (ValueError, TypeError):
                pass


class UploadForm(forms.Form):
    file = forms.FileField(required=True)

