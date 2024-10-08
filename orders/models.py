from django.db import models
from django.core.exceptions import ValidationError
from tables.models import Table
from menu.models import Dish

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    order_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('da confermare', 'Da confermare'),('confermato', 'Confermato')], default='da confermare')
 
    def __str__(self):
        if self.table is None:
            return f'Ordine {self.id}'
        return f'Ordine {self.id} per il tavolo {self.table.table_number}'


    @property
    def total_price(self):
        return sum(detail.total_price for detail in self.order_details.all())


def validate_positive_nonzero(value):
    if value <= 0:
        raise ValidationError(
            '%(value)s non è un valore valido. La quantità deve essere maggiore di zero.',
            params={'value': value},
        )

class OrderDetail(models.Model):
    STATUS_CHOICES = [
        ('In attesa', 'In attesa'),
        ('In preparazione', 'In preparazione'),
        ('Pronto', 'Pronto')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)    
    quantity = models.PositiveIntegerField(default=1, validators=[validate_positive_nonzero])
    status = models.CharField(max_length=20, choices= STATUS_CHOICES , default='In attesa')

    def __str__(self):
        return f'{self.quantity} x {self.dish.name} Stato: {self.status}'
    @property
    def total_price(self):
        return self.dish.price * self.quantity
    @property
    def total_earned(self):
        return self.dish.profit * self.quantity
    @property
    def status_choices(self):
        return self.STATUS_CHOICES
    @property
    def move_to_next_status(self):
        current_index = self.get_status_index(self.status) # Ottiene l'indice dello stato corrente
        next_index = (current_index + 1) % len(self.STATUS_CHOICES)  # Calcola l'indice del prossimo stato
        self.status = self.STATUS_CHOICES[next_index][0]  # Assegna il prossimo stato

    def get_status_index(self, status):
    # con la list comprehension ottengo la lista degli stati, in seguito chiamo il metodo index() per ottenere l'indice dello stato passato come argomento
        return [s[0] for s in self.STATUS_CHOICES].index(status)
    
    
class SimilarityMatrix(models.Model):
    dish1 = models.ForeignKey(Dish, related_name='similarity_dish1', on_delete=models.CASCADE)
    dish2 = models.ForeignKey(Dish, related_name='similarity_dish2', on_delete=models.CASCADE)
    similarity = models.FloatField()
    
class CoOccurrenceMatrix(models.Model):
    dish1 = models.ForeignKey(Dish, related_name='cooccurrence_dish1', on_delete=models.CASCADE)
    dish2 = models.ForeignKey(Dish, related_name='cooccurrence_dish2', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

