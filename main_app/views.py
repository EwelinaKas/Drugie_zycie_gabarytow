from django.shortcuts import render, redirect
from main_app.models import Product, ShoppingCart, ShoppingCartItem, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddProduct
from decimal import Decimal


def home(request):
    return render(request,
                  'main_app/home.html')


def auction_view(request):
    products = Product.objects.all()
    return render(request, 'main_app/product_list.html', context={'products': products})


def product_detail_view(request, pk):
    product = Product.objects.get(id=pk)
    if product.quantity == 0:
        messages.info(request, 'Przykro nam, aktualnie brak tego produktu')
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
        product.quantity -= 1
        product.save()
        if cart_item in show_cart:
            cart_item.qty += 1
        cart_item.save()

    except ShoppingCartItem.DoesNotExist:
        cart_item = ShoppingCartItem.objects.create(product_item=product, cart_id=cart)
        product.quantity -= 1
        product.save()
        cart_item.save()

    context = {'cart': cart, 'product': product, 'cart_item': cart_item, 'show_cart': show_cart}
    return render(request, 'main_app/shopping_cart.html', context=context)


@login_required
def cart_view(request):
    cart = get_user_shopping_cart(request)
    show_cart = ShoppingCartItem.objects.filter(cart_id=cart)
    order_total = Decimal(0.0)
    buy = buy_now(request)
    if buy:
        return render(request, 'main_app/order_complete.html')

    for item in show_cart:
        order_total += item.product_item.price * item.qty

    return render(request, 'main_app/cart_view.html',
                  context={'show_cart': show_cart, 'order_total': order_total})


@login_required
def users_products(request):

    product = Product.objects.filter(user=request.user)
    return render(request, 'main_app/user_products.html', context={'product':product})


def update_product(request, pk):
    product_to_update = Product.objects.get(id=pk)
    update_form = AddProduct(request.POST or None, request.FILES or None, instance=product_to_update)
    if request.method == 'GET':
        return render(request, 'main_app/update_product.html',
                      context={'update_form': update_form, 'product_to_update': product_to_update})

    if request.method == 'POST':
        update_form.save()
        return redirect('main_app:auctions')


def buy_now(request):

    cart = get_user_shopping_cart(request)
    show_cart = ShoppingCartItem.objects.filter(cart_id=cart)

    if request.method == 'POST':
        bought = request.POST.get('buy')

        if bought:
            show_cart.delete()
        return redirect('main_app:order_complete')


def search_by_category(request):
    search_query = request.GET.get('q')
    results = Category.objects.filter(name__icontains=search_query)
    # category = Category.objects.all()[0]
    # prodcat = Product.objects.filter(['category'])

    return render(request, 'main_app/search.html', context={'results': results } )


def delete_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'GET':
        return render(request, 'main_app/delete_product.html', context={'product': product})

    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm:
            product.delete()

    return redirect('main_app:user_products')


# def remove_item(request):
#     cart = get_user_shopping_cart(request)
#     show_cart = ShoppingCartItem.objects.filter(cart_id=cart)
#     cart_item = ShoppingCartItem.objects.get(product_item=product, cart_id=cart)
#     if request.method == 'POST':
#         remove = request.POST.get('buy')
#         if remove:
#             product.quantity += cart_item.qty
#             cart_item.qty = 0
#             product.save()
#             cart_item.delete()
#
#     return redirect('main_app:auctions')


