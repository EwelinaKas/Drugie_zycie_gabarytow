from django.contrib import admin

from main_app.models import Product, ShoppingCart, ShoppingCartItem, Category, \
   Order, OrderItem


admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)