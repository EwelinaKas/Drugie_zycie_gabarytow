from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.name}, {self.price}'


class Category(models.Model):
    parent_category_id = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty_in_stock = models.IntegerField()
    product_image = models.ImageField(blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ShoppingCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class ShoppingCartItem(models.Model):
    cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product_item_id = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    qty = models.IntegerField()




