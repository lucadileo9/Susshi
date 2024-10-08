from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from tables.models import Table
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

   
class TableCreationForm(UserCreationForm):
    table_number = forms.IntegerField(label="Numero del tavolo")
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'table_number']
        error_messages = {
            'username': {
                'unique': "Nome già esistente!!! Non è possibile avere due tavoli con lo stesso nome.",
            },
        }
        
    def clean_table_number(self):
        table_number = self.cleaned_data.get('table_number')
        if Table.objects.filter(table_number=table_number).exists():
            raise ValidationError("Numero già esistente!!! Non è possibile avere due tavoli con lo stesso numero.")
        return table_number
    
    def save(self, commit=True):
        # Salva l'utente e restituisce l'oggetto User
        user = super().save(commit) 
        # Ottiene il gruppo "Tavolo" e aggiunge l'utente
        g = Group.objects.get(name="Tavolo") 
        g.user_set.add(user) 
        # Ottiene il numero del tavolo
        table_number = self.cleaned_data.get('table_number')
        # Crea un oggetto Table associato all'utente
        Table.objects.create(user=user, table_number=table_number)
        
        return user

class ChefCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit) 
        g = Group.objects.get(name="Chef") 
        g.user_set.add(user) 
        return user
    

