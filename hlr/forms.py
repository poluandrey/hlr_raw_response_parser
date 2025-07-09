from django import forms
from django.core.exceptions import ValidationError

from hlr.models import Task, HlrProduct


class TaskCreateForm(forms.ModelForm):
    msisdn = forms.CharField(required=False)
    file = forms.FileField(required=False)
    hlr = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'hlr-box'}),
        queryset=HlrProduct.objects.filter(type__icontains='hlr'),
        label="HLR products"
    )
    mnp = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mnp-box'}),
        queryset=HlrProduct.objects.filter(type__icontains='mnp'),
        label="MNP products"
    )

    def clean(self):
        cleaned_data = super().clean()
        hlr = cleaned_data.get('hlr')
        mnp = cleaned_data.get('mnp')

        self._custom_errors = []

        if not (cleaned_data.get('msisdn') or cleaned_data.get('file')):
            self._custom_errors.append("fill msisdn or upload file")

        if not any([mnp, hlr]):
            self._custom_errors.append("choose source")

        # Возвращаем ValidationError, чтобы форма была невалидна
        if self._custom_errors:
            raise ValidationError(" ")

    class Meta:
        model = Task
        fields = ['msisdn', 'file', 'hlr', 'mnp']

    class Media:
        css = {
            'all': ('admin/css/custom_task.css',)
        }

# class TaskCreateForm(forms.ModelForm):
#     msisdn = forms.CharField(required=False)
#     file = forms.FileField(required=False)
#     hlr = forms.ModelMultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple(attrs={
#             'class': 'hlr-box',
#         }),
#         queryset=HlrProduct.objects.filter(type__icontains='hlr'),
#         label="HLR products"
#     )
#
#     mnp = forms.ModelMultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple(attrs={
#             'class': 'mnp-box',
#         }),
#         queryset=HlrProduct.objects.filter(type__icontains='mnp'),
#         label="MNP products"
#     )
#
#     # def clean(self):
#     #     cleaned_data = super().clean()
#     #     hlr = cleaned_data.get('hlr')
#     #     mnp = cleaned_data.get('mnp')
#     #     if not (cleaned_data.get('msisdn') or cleaned_data.get('file')):
#     #         raise ValidationError('fill msisdn or upload file')
#     #
#     #     if not any([mnp, hlr]):
#     #         raise ValidationError('choose source')
#
#     def clean(self):
#         cleaned_data = super().clean()
#         hlr = cleaned_data.get('hlr')
#         mnp = cleaned_data.get('mnp')
#         if not (cleaned_data.get('msisdn') or cleaned_data.get('file')):
#             self._custom_errors.append("fill msisdn or upload file")
#
#         if not any([mnp, hlr]):
#             self._custom_errors.append("choose source")
#
#         if self._custom_errors:
#             raise ValidationError(" ")
#
#     class Meta:
#         model = Task
#         fields = [
#             'msisdn',
#             'file',
#             'hlr',
#             'mnp',
#         ]
#
#     class Media:
#         css = {
#             'all': ('admin/css/custom_task.css',)
#         }
