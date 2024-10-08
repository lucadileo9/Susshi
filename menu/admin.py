from django.contrib import admin
from .models import Dish, Ingredient

admin.site.register(Ingredient)
admin.site.register(Dish)
