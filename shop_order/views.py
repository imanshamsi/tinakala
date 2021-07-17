from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from zeep import Client

from shop_accounts.models import UserProfile
from shop_cart.sessions import Cart
from shop_order.forms import OrderUserAddress
from shop_order.models import Order, OrderItem, Invoice
from shop_products.models import ProductAmazing
from tinakala.utils import profile_completion_required, verify_phone_required


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
@verify_phone_required(profile_model=UserProfile, redirected_path='auth:verify-phone')
def cart_check_out(request):
    cart = Cart(request)
    address_form = OrderUserAddress(request.POST or None, request=request)
    if request.method == 'POST' and address_form.is_valid() and len(cart) != 0:
        order = Order.objects.create(customer=request.user, address=address_form.cleaned_data.get('user_address'))
        for item in cart:
            amazing: ProductAmazing = ProductAmazing.objects.filter(product=item['product']).first()
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_price=amazing.get_price() if amazing else item['price'],
                product_count=item['product_count'],
                product_cost=Decimal(item['product_count']) * Decimal(amazing.get_price() if amazing else item['price'])
            )
        products = OrderItem.objects.filter(order=order)
        total_price = order.get_nice_total_price()
        cart.clear()
        return render(request, 'order/SiteOrderDetail.html', {'order': order, 'products': products, 'total_price': total_price, })
    context = {
        'cart': cart,
        'address_form': address_form,
    }
    return render(request, 'order/SiteUserCheckOut.html', context)


client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
merchant = '0007cbe5-6ad3-4646-ba63-c1e06f864410'


def to_bank(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    amount = 0
    order_items = OrderItem.objects.filter(order=order)
    for product in order_items:
        amount += product.product_cost

    callbackUrl = 'http://127.0.0.1:8000/callback/'
    mobile = ''
    email = ''
    description = ''
    result = client.service.PaymentRequest(merchant, amount, description, email, mobile, callbackUrl)

    if result.Status == 100 and len(result.Authority) == 36:
        Invoice.objects.create(order=order, authority=result.Authority)
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return HttpResponse('Error code ' + str(result.Status))


def call_back(request):
    if request.GET.get('Status') == 'OK':
        authority = request.GET.get('Authority')
        invoice = get_object_or_404(Invoice, authority=authority)
        amount = 0
        order = invoice.order
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            amount += item.product_cost
        result = client.service.PaymentVerification(merchant, authority, amount)
        if result.Status == 100:
            return render(request, 'order/SiteOrderCallBack.html', {'invoice': invoice})
        else:
            return HttpResponse('error ' + str(result.Status))
    else:
        return HttpResponse('error ')
