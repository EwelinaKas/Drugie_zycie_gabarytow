from django.shortcuts import render, redirect
from main_app.models import Product, ShoppingCart, ShoppingCartItem
from django.contrib.auth.decorators import login_required
from .forms import AddProduct
from decimal import Decimal

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


def get_user_shopping_cart(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        try:
            cart = ShoppingCart.objects.get(user_id=request.user)
            cart.save()

        except ShoppingCart.DoesNotExist:
            cart = ShoppingCart(user_id=request.user)
            cart.save()

    return cart

@login_required
def add_to_shopping_cart(request, pk):
    cart = get_user_shopping_cart(request)
    product = Product.objects.get(id=pk)
    show_cart = ShoppingCartItem.objects.filter(cart_id=cart)

    try:
        cart_item = ShoppingCartItem.objects.get(product_item=product, cart_id=cart)
        if cart_item in show_cart:
            cart_item.qty += 1
        cart_item.save()

        cart_item.save()
    except ShoppingCartItem.DoesNotExist:
        cart_item = ShoppingCartItem.objects.create(product_item=product, cart_id=cart)
        cart_item.save()

    context = {'cart': cart, 'product': product, 'cart_item': cart_item, 'show_cart': show_cart}

    return render(request, 'main_app/shopping_cart.html', context=context)

@login_required
def cart_view(request):
    cart = get_user_shopping_cart(request)
    show_cart = ShoppingCartItem.objects.filter(cart_id=cart)
    order_total = Decimal(0.0)
    for item in show_cart:
        order_total += item.product_item.price * item.qty
    return render(request, 'main_app/cart_view.html', context={'show_cart': show_cart, 'order_total': order_total})


@login_required
def users_products(request):

    product = Product.objects.filter(user=request.user)

    return render(request, 'main_app/user_products.html', context={'product':product})


def update_product(request, pk):
    product_to_update = Product.objects.get(id=pk)
    update_form = AddProduct(request.POST or None, instance=product_to_update)
    if request.method == 'GET':
        return render(request, 'main_app/update_product.html',
                      context={'update_form': update_form, 'product_to_update': product_to_update})

    if request.method == 'POST':
        update_form.save()
        return redirect('main_app:auctions')


