from django import forms
from .models import Order
from order.models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','phone','email','address_line1','address_line2','state','city','order_note']
        
class OrderStatus(forms.ModelForm):
    class Meta:
        model=Order
        fields=['status']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields=['subject','review','rating']