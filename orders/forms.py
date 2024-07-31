from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'mobile_no','email', 'address_1', 'address_2', 'street', 'city',
                  'district', 'state', 'country', 'pincode','order_note']
