from django.shortcuts import render, redirect
from main_app.models import Product
from django.contrib.auth.decorators import login_required
from .forms import AddProduct

# Create your views here.


def home(request):
    return render(request,
                  'main_app/home.html')


def auction_view(request):
    products = Product.objects.all()
    return render(request, 'main_app/product_list.html', context={'products': products})


def product_detail_view(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'main_app/product_detail.html', context={'product': product})


@login_required(login_url='accounts:login')
def add_product(request):

    form = AddProduct(request.POST or None, request.FILES)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return redirect('main_app:auctions')

    return render(request, 'main_app/add_product.html', context={'form': form})






    # form = AddProduct(request.POST or None)
    # if form.is_valid():
    #     form = form.save(commit=False)
    #     form.user = request.user
    #     form.save()
    #
    # return render(request, 'main_app/home.html', context={'form': form})






