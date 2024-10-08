from django.shortcuts import render, redirect
from .forms import *
from .models import RestaurantInfo, ContactInfo
from django.contrib.auth.decorators import user_passes_test

def homepage(request):
    restaurant_info = RestaurantInfo.objects.first()
    if not restaurant_info: # Se non esiste un oggetto RestaurantInfo, creane uno di default
        restaurant_info = {
            'name': 'Susshi House',
            'address': '123 Sushi St, Modena, Italia',
            'image': '/sushi.jpg',}
    return render(request, 'restaurant/home.html', context={'restaurant_info': restaurant_info})

def about_us(request):
    contact_info = ContactInfo.objects.first()
    if not contact_info: # Se non esiste un oggetto ContactInfo, creane uno di default
        contact_info = {
            'phone': '+39 123 456 7890',
            'email': 'info@sushihouse.it',
            'description': "In una tranquilla strada nel cuore di Modena, c'era un giovane chef italiano... ecc...gliente.",
        }
    return render(request, 'restaurant/about_us.html', context={'contact_info': contact_info})


def is_chef(user):
    return user.groups.filter(name='Chef').exists()

@user_passes_test(is_chef)
def edit_restaurant_info(request):
    restaurant_info = RestaurantInfo.objects.first()
    if request.method == 'POST':
        form = RestaurantInfoForm(request.POST, request.FILES, instance=restaurant_info)
        if form.is_valid():
            form.save()
            return redirect('restaurant:homepage')
    else:
        form = RestaurantInfoForm(instance=restaurant_info)
    return render(request, 'restaurant/restaurant_info_update.html', {'form': form})

@user_passes_test(is_chef)
def edit_about_us(request):
    contact_info = ContactInfo.objects.first()
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=contact_info)
        if form.is_valid():
            form.save()
            return redirect('restaurant:about_us')
    else:
        form = ContactInfoForm(instance=contact_info)
    return render(request, 'restaurant/about_us_update.html', {'form': form})

