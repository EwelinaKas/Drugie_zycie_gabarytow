from django.urls import path

from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),

    # PRODUCT
    path('auctions/', views.auction_view, name='auctions'),
    path('<int:pk>/', views.product_detail_view, name='product_detail_view'),
    path('add/', views.add_product, name='add'),
    path('search/', views.search_by_name, name='search'),

    # USER
    path('user_products/', views.users_products, name='user_products'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),

    # CART
    path('cart/<int:pk>/', views.add_to_shopping_cart, name='add_to_shopping_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('order_complete/', views.buy_now, name='order_complete'),
    path('remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('update_cart/<int:pk>/', views.update_cart, name='update_cart'),

    #ORDER_VIEW
    path('orders/', views.orders, name='orders'),

]
