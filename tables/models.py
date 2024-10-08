from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    table_number = models.PositiveIntegerField(unique=True, error_messages={
            'unique': "Numero già esistente!!! Non è possibile avere due tavoli con lo stesso numero.",
        })
    
    def delete(self, *args, **kwargs):
        # Cancella l'utente associato prima di cancellare il tavolo
        self.user.delete()
        # Cancella il tavolo
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f'Tavolo {self.user.username} N° {self.table_number}'

