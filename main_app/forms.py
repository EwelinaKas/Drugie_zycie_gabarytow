from django import forms
from .models import Product


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'photo',
            'quantity',
            'category',
        ]





