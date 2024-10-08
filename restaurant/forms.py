from django import forms
from .models import RestaurantInfo, ContactInfo

class RestaurantInfoForm(forms.ModelForm):
    class Meta:
        model = RestaurantInfo
        fields = ['name', 'address', 'image']

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['phone', 'email', 'description']
     