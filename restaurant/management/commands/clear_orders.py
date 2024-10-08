from django.core.management.base import BaseCommand
from orders.models import Order

class Command(BaseCommand):
    help = 'Cancella tutti gli ordini'

    def handle(self, *args, **kwargs):
        Order.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Ordini cancellati con successo.'))
