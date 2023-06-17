from django.shortcuts import render, redirect
from main_app.models import Product, ShoppingCart, ShoppingCartItem, Category, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddProduct
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request,
                  'main_app/home.html')


def auction_view(request):
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.get_all_products_by_category_id(category_id)
    else:
        products = Product.objects.all()

    return render(request, 'main_app/product_list.html', context={'products': products, 'categories': categories})


def product_detail_view(request, pk):
    product = Product.objects.get(id=pk)
    if product.quantity == 0:
        messages.info(request, 'Sorry, this product is out of stock')
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
        if cart_item.qty < cart_item.product_item.quantity:
            cart_item.product_item.quantity -= 1
            cart_item.qty += 1
        cart_item.product_item.save()
        cart_item.save()

    except ShoppingCartItem.DoesNotExist:
        cart_item = ShoppingCartItem.objects.create(product_item=product, cart_id=cart)
        cart_item.product_item.quantity -= 1
        cart_item.product_item.save()
        cart_item.save()

    context = {'cart': cart, 'product': product, 'cart_item': cart_item, 'show_cart': show_cart}
    return render(request, 'main_app/shopping_cart.html', context=context)


@login_required
def cart_view(request):
    cart = get_user_shopping_cart(request)
    show_cart = ShoppingCartItem.objects.filter(cart_id=cart)
    order_total = Decimal(0.0)
    buy = buy_now(request)
    total_quantity = 0
    if buy:
        return render(request, 'main_app/order_complete.html', context={'show_cart': show_cart})

    for item in show_cart:
        order_total += item.product_item.price * item.qty

    for quantity in show_cart:
        total_quantity += quantity.qty

    return render(request, 'main_app/cart_view.html',
                  context={'show_cart': show_cart, 'order_total': order_total, 'total_quantity': total_quantity})


@login_required
def users_products(request):

    product = Product.objects.filter(user=request.user)
    return render(request, 'main_app/user_products.html', context={'product': product})


def update_product(request, pk):
    product_to_update = Product.objects.get(id=pk)
    update_form = AddProduct(request.POST or None, request.FILES or None, instance=product_to_update)
    if request.method == 'GET':
        return render(request, 'main_app/update_product.html',
                      context={'update_form': update_form, 'product_to_update': product_to_update})

    if request.method == 'POST':
        if update_form.is_valid():
            update_form.save()
        else:
            messages.error(request, "You can't add negative value")
            return render(request, 'main_app/update_product.html')
        return redirect('main_app:auctions')


def buy_now(request):
    order_init = start_order(request)
    cart = get_user_shopping_cart(request)
    show_cart = ShoppingCartItem.objects.filter(cart_id=cart)
    if request.method == 'POST':
        bought = request.POST.get('buy')

        for order_item in show_cart:
            ord_itm = OrderItem.objects.create(order=order_init, product=order_item.product_item.name,
                                               quantity=order_item.qty)
            ord_itm.save()

        if bought:
            show_cart.delete()
        return redirect('main_app:order_complete')


def search_by_name(request):
    search_query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=search_query)
    return render(request, 'main_app/search.html', context={'results': results})


def delete_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'GET':
        return render(request, 'main_app/delete_product.html', context={'product': product})

    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm:
            product.delete()

    return redirect('main_app:user_products')


def cart_remove(request, pk):
    cart = get_user_shopping_cart(request)
    product = Product.objects.get(id=pk)
    cart_item = ShoppingCartItem.objects.get(product_item=product, cart_id=cart)
    if cart_item.qty > 0:
        cart_item.qty -= 1
        cart_item.save()
        cart_item.product_item.quantity += 1
        cart_item.product_item.save()

    if cart_item.qty == 0:
        cart_item.delete()
    return redirect("main_app:cart_view")


def update_cart(request, pk):

    cart = get_user_shopping_cart(request)
    product = Product.objects.get(id=pk)
    cart_item = ShoppingCartItem.objects.get(product_item=product, cart_id=cart)
    if cart_item.product_item.quantity > 0:
        cart_item.product_item.quantity -= 1
        cart_item.qty += 1
        cart_item.save()
        cart_item.product_item.save()
    else:
        messages.error(request, 'Sorry, there is no more this product in our auction right now')

    return redirect('main_app:cart_view')


def start_order(request):
    try:
        order = Order.objects.get(customer=request.user)
        order.save()
    except ObjectDoesNotExist:
        order = Order.objects.create(customer=request.user)
        order.save()
    return order


def orders(request):
    order = Order.objects.get(customer=request.user)
    order_view = OrderItem.objects.filter(order=order)
    return render(request, 'main_app/orders.html', context={'order_view': order_view})
