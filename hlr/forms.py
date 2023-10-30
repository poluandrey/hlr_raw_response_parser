from django import forms

from hlr.models import Task, HlrProduct


class TaskCreateForm(forms.ModelForm):
    msisdn = forms.CharField()
    hlr = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=HlrProduct.objects.all().values_list('product__external_product_id',
                                                     'product__description'),
    )

    class Meta:
        model = Task

        fields = [
            'msisdn',
            'hlr',
        ]
        widgets = {
            'msisdn': forms.TextInput,
            'hlr': forms.MultipleChoiceField(
                required=False,
                widget=forms.CheckboxSelectMultiple,
                choices=HlrProduct.objects.all().values_list('id', 'product__description'),
            ),
        }
