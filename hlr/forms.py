from django import forms
from django.core.exceptions import ValidationError

from hlr.models import Task, HlrProduct


class TaskCreateForm(forms.ModelForm):
    msisdn = forms.CharField(required=False)
    file = forms.FileField(required=False)
    hlr = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'hlr-checkbox-select-multiply',
        }),
        queryset=HlrProduct.objects.filter(type__icontains='hlr'),
        label="HLR продукты"
    )

    mnp = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'mnp-checkbox-select-multiply',
        }),
        queryset=HlrProduct.objects.filter(type__icontains='mnp'),
        label="MNP продукты"
    )

    def clean(self):
        cleaned_data = super().clean()
        hlr = cleaned_data.get('hlr')
        mnp = cleaned_data.get('mnp')

        if not (cleaned_data.get('msisdn') or cleaned_data.get('file')):
            raise ValidationError('fill msisdn or upload file')

        if not mnp or hlr:
            raise ValidationError('choose source')

    class Meta:
        model = Task
        fields = [
            'msisdn',
            'hlr',
            'file',
        ]
