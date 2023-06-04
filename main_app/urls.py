from django.urls import path

from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('auctions/', views.auction_view, name='auctions'),
    path('<int:pk>/', views.product_detail_view, name='product_detail_view'),
    path('add/', views.add_product, name='add'),


]
