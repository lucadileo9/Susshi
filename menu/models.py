from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, error_messages={
            'unique': "Nome già esistente!!! Non è possibile avere due ingreidenti con lo stesso nome.",
        })
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True, error_messages={
            'unique': "Nome già esistente!!! Non è possibile avere due piatti con lo stesso nome.",
        })
    description = models.TextField()
    
    price = models.FloatField(blank=False, validators=[MinValueValidator(0.01)])
    ingredients = models.ManyToManyField(Ingredient, related_name='dishes')
    profit = models.FloatField(blank=False, validators=[MinValueValidator(0.01)])
    image = models.ImageField(upload_to='dish_images/', blank=True, null=True)

    def __str__(self):
        return self.name
