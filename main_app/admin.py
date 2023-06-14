from django.contrib import admin

from main_app.models import Product, ShoppingCart, ShoppingCartItem, Category, Variation, VariationOption, ProductConfiguration


admin.site.register(Product)
# admin.site.register(ProductItem)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Variation)
admin.site.register(VariationOption)
admin.site.register(ProductConfiguration)
admin.site.register(Category)
