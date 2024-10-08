from django import forms
from .models import Ingredient, Dish
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class DishSearchForm(forms.Form):
    name = forms.CharField(label='Nome del piatto', max_length=100, required=False)
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        label='Ingredienti',
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    max_price = forms.DecimalField(label='Prezzo massimo', max_digits=10, decimal_places=2, required=False, min_value=1)

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
        widgets = {
            'ingredients': forms.CheckboxSelectMultiple
        }
    price = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        label='Prezzo',
        error_messages={
            'min_value': 'Il prezzo deve essere maggiore di 0.01',
        }

    )
    profit = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)], 
        label='Profitto',
        error_messages={
            'min_value': 'Il profitto deve essere maggiore di 0.01',
        }
    )




