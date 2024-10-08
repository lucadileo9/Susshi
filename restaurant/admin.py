from django.contrib import admin
from .models import RestaurantInfo, ContactInfo

# Register your models here.
admin.site.register(RestaurantInfo)
admin.site.register(ContactInfo)
