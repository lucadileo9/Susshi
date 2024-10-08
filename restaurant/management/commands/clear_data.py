from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from menu.models import Ingredient, Dish
from tables.models import Table
from orders.models import Order, OrderDetail, CoOccurrenceMatrix, SimilarityMatrix
from restaurant.models import RestaurantInfo, ContactInfo
class Command(BaseCommand):
    help = 'Clear all data from Ingredient, Dish, and Table models'

    def handle(self, *args, **kwargs):
        # Delete data from custom models
        Ingredient.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from Ingredient model'))

        Dish.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from Dish model'))
        
        Table.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from Table model'))
        
        RestaurantInfo.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from RestaurantInfo model'))
        
        ContactInfo.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from ContactInfo model'))
        
        Order.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from Order model'))
        
        OrderDetail.objects.all().delete()  
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from OrderDetail model')) 
        
        SimilarityMatrix.objects.all().delete() 
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from SimilarityMatrix model'))
        
        CoOccurrenceMatrix.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from CoOccurrenceMatrix model'))      
                 
        # Delete all users except the superuser
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all users except the superuser'))

        self.stdout.write(self.style.SUCCESS('Successfully cleared all data'))
