from django import forms
from .models import Order



class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 
        'postal_code', 'city', 'area', 'estate']

# This is the form that you are going to use to create new Order objects.