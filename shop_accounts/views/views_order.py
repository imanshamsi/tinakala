"""
shop_accounts -> views -> user order history, support methods
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from pure_pagination import PageNotAnInteger, Paginator

from shop_accounts.models import UserProfile
from shop_order.models import Order, OrderItem
from shop_products.models import ProductAmazing
from tinakala.utils import profile_completion_required, verify_phone_required


@login_required(login_url='auth:login')
def user_profile_summary_last_orders(request):
    orders = []
    for index, order in enumerate(Order.objects.filter(customer=request.user).order_by('-order_date')):
        service_check_order(order.order_code)
        orders.append({
            'id': index + 1,
            'detail': order,
        })
    context = {
        'orders': orders[:5],
    }
    return render(request, 'accounts/component/profile_user_last_orders.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
@verify_phone_required(profile_model=UserProfile, redirected_path='auth:verify-phone')
def user_orders(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    orders = []
    for index, order in enumerate(Order.objects.filter(customer=request.user).order_by('-order_date')):
        service_check_order(order.order_code)
        orders.append({
            'id': index + 1,
            'detail': order,
        })
    paginated_order = Paginator(orders, request=request, per_page=7).page(page)
    context = {
        'orders': paginated_order,
    }
    return render(request, 'accounts/SiteUserOrders.html', context)


def service_check_order(order_code):
    order = get_object_or_404(Order, order_code=order_code)
    if not order.is_paid:
        order_items = order.orderitem_set.all()
        for item in order_items:
            product = item.product
            amazing = ProductAmazing.objects.filter(product=product).first()
            order_item = OrderItem.objects.get(pk=item.id)
            if not amazing:
                if product.price != item.product_price:
                    order_item.product_price = product.price
                    order_item.save()
            else:
                if amazing.get_price != item.product_price:
                    order_item.product_price = amazing.get_price()
                    order_item.save()
            if product.inventory == 0:
                order_item.delete()
            elif product.inventory < item.product_count:
                order_item.product_count = product.inventory
                order_item.save()
        return True
    return False


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
@verify_phone_required(profile_model=UserProfile, redirected_path='auth:verify-phone')
def user_order_detail(request, order_code):
    service_check_order(order_code=order_code)
    order = get_object_or_404(Order, order_code=order_code)
    items = order.orderitem_set.all()
    structured_items = []
    amount = 0
    for item in items:
        amount += item.product_cost
        amazing = ProductAmazing.objects.filter(product=item.product).first()
        structured_items.append({
            'product_avatar_url': item.product.avatar.url,
            'product_code': item.product.code,
            'product_slug': item.product.slug,
            'product_title': item.product.title,
            'product_count': item.product_count,
            'product_amazing': amazing,
            'get_nice_price': item.get_nice_price(),
            'get_nice_total_price': item.get_nice_total_price(),
        })
    context = {
        'order': order,
        'items': structured_items,
        'order_count': len(items),
        'total_price': f'{amount:,}',
    }
    return render(request, 'accounts/SiteUserOrderDetail.html', context)
