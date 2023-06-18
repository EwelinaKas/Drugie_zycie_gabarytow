from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.name}, {self.price}'

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter (category=category_id)
        else:
            return Product.objects.all()


class Category(models.Model):
    parent_category_id = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


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


class Order(models.Model):
    customer = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)



