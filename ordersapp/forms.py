from django import forms
from django.forms import ModelForm
from ordersapp.models import Order


class OrderForm(forms.Modelform):
    class Meta:
        models = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Цена', required=False)

    class Meta:
        models = Order
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
