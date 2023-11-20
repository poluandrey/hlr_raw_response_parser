from django import forms
from django.core.exceptions import ValidationError

from hlr.models import Task, HlrProduct


class TaskCreateForm(forms.ModelForm):
    msisdn = forms.CharField(required=False)
    file = forms.FileField(required=False)
    hlr = forms.ModelMultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={}),
        queryset=HlrProduct.objects,

    )

    def clean(self):
        cleaned_data = super().clean()

        if not (cleaned_data.get('msisdn') or cleaned_data.get('file')):
            raise ValidationError('fill msisdn or upload file')

    class Meta:
        model = Task
        fields = [
            'msisdn',
            'hlr',
            'file'
        ]
