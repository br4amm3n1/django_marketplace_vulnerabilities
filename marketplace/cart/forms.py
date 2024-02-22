from django import forms
from .models import Purchase


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['delivery_address']

    delivery_address = forms.CharField(
        label='Адрес доставки:',
        max_length=255,
        required=True
    )
