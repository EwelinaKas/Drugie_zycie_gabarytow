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
            'category',



        ]

    def __repr__(self):
        return self.fields
