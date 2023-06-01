from django.shortcuts import render
from main_app.models import Product
from .forms import AddProduct

# Create your views here.


def home(request):
    return render(request,
                  'main_app/home.html')


def auction_view(request):
    products = Product.objects.all()
    return render(request, 'main_app/product_list.html', context={'products': products})


