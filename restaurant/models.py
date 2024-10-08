from django.db import models

class RestaurantInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='', blank=True, null=True)
  
class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()