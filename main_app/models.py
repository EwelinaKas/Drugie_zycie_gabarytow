from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.name}, {self.price}'


class Category(models.Model):
    parent_category_id = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class ProductItem(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
#     qty_in_stock = models.IntegerField()
#     product_image = models.ImageField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return str(self.product)


class ShoppingCart(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)


class ShoppingCartItem(models.Model):
    cart_id = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)
    product_item = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return str(self.product_item)


class Variation(models.Model):

    VAR_CHOICES = (('materiał', 'materiał'), ('rozmiar', 'rozmiar'))

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, choices=VAR_CHOICES)

    def __str__(self):
        return self.name


class VariationOption(models.Model):
    variation = models.ForeignKey('Variation', on_delete=models.CASCADE)
    value = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.value


class ProductConfiguration(models.Model):
    product_item = models.ForeignKey('Product', on_delete=models.CASCADE)
    variation_option = models.ForeignKey('VariationOption', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.variation_option)
