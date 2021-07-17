from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from shop_cart.sessions import Cart
from shop_cart.forms import AddProductToCart
from shop_products.models import Product


def cart_view(request):
    cart = Cart(request)
    for item in cart:
        item['update_product_count_form'] = AddProductToCart(
            initial={
                'product_count': item['product_count'],
                'update': True,
            }, inventory=item['product'].inventory)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/SiteCartDetail.html', context)


@require_POST
def cart_add(request, product_code):
    cart = Cart(request)
    product = get_object_or_404(Product, code=product_code)
    form = AddProductToCart(request.POST, inventory=product.inventory)
    if form.is_valid():
        if product.status:
            data = form.cleaned_data
            if not data['product_count']:
                data['product_count'] = 1
            cart.add(product=product, product_count=data['product_count'], update_count=data['update'])
        else:
            cart.remove(product)
    return redirect('cart:user-cart')


def cart_remove(request, product_code):
    cart = Cart(request)
    product = get_object_or_404(Product, code=product_code)
    cart.remove(product)
    return redirect('cart:user-cart')
