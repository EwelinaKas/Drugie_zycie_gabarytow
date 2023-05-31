from django.contrib import admin

from main_app.models import Product, ProductItem, ShoppingCart, ShoppingCartItem, Category


admin.site.register(Product)
admin.site.register(ProductItem)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Category)
