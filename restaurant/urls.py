from django.urls import path,re_path
from .views import *
app_name = 'restaurant'
urlpatterns = [
    re_path(r"^$|^/$|^home/$", homepage, name="homepage"),
    path('about/', about_us, name='about_us'),
    path('edit_restaurant_info/', edit_restaurant_info, name='edit_restaurant_info'),
    path('edit_contact_info/', edit_about_us, name='edit_contact_info'),
]

