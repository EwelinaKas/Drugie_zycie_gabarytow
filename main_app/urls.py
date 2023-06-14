from django.urls import path

from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('auctions/', views.auction_view, name='auctions'),
    path('<int:pk>/', views.product_detail_view, name='product_detail_view'),
    path('add/', views.add_product, name='add'),
    path('cart/<int:pk>/', views.add_to_shopping_cart, name='add_to_shopping_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('user_products/', views.users_products, name='user_products'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('order_complete/', views.buy_now, name='order_complete'),





]
