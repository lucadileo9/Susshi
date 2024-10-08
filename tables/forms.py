from django import forms
from .models import Table
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

# Questa classe mixin controlla se l'utente è il proprietario del tavolo oppure se è uno chef
class UserIsTableOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        table = self.get_object()
        
        if table.user != request.user and not request.user.groups.filter(name='Chef').exists()  :
            raise PermissionDenied            
        return super().dispatch(request, *args, **kwargs)
# N.B.: Questo mixin è stato utilizzato nella vista TableDetailView, e dovrebbe essere in un file specifico detto mixins.py
# ma l'ho messo qui per comodità


class TableUpdateForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Nuova Password", required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Conferma Password", required=False, widget=forms.PasswordInput)
    table_number = forms.IntegerField(label="Numero del tavolo")

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'table_number']

    def __init__(self, *args, **kwargs):
        # Recupero l'istanza del tavolo passata come argomento
        self.table_instance = kwargs.pop('table_instance')
        super().__init__(*args, **kwargs)
        # Inizializzo i campi con i valori attuali
        self.fields['username'].initial = self.table_instance.user.username
        self.fields['table_number'].initial = self.table_instance.table_number

    # Questo metodo controlla se il nome utente è già in uso
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.table_instance.user.pk).exists():
            raise ValidationError("Questo nome utente è già in uso. Scegli un altro nome utente.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        # Controllo se le password corrispondono
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            self.add_error('confirm_password', "Le password non corrispondono.")
        return cleaned_data
    
    def save(self, commit=True):
        # ottengo l'utente daò tavolo
        user = self.table_instance.user
        # ne modifico l'username e la password
        user.username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if password:
            user.set_password(password)
        if commit:
            # salvo l'utente e il tavolo
            user.save()
            table = self.table_instance
            table.table_number = self.cleaned_data.get('table_number')
            table.save()
        
        return table
