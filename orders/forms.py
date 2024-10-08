from django import forms
from .models import OrderDetail

# class AddDishForm(forms.ModelForm):
#     class Meta:
#         model = OrderDetail
#         fields = ['quantity']

class AddDishForm(forms.ModelForm):
    quantity = forms.IntegerField(
        label="Quantità",
        min_value=1,  # Assicura che il campo del modulo non accetti valori minori di 1
        initial=1,  # Imposta il valore iniziale del campo del modulo a 1
    )

    class Meta:
        model = OrderDetail
        fields = ['quantity']

class ConfirmOrderForm(forms.Form):
    confirm = forms.BooleanField(required=True, label="Conferma ordine")
