from django.shortcuts import render
from django.contrib import messages

from shop_accounts.models import UserFavorite
from shop_cart.sessions import Cart
from shop_categories.models import SubCategoryParent, Brands
from shop_contact.models import UserTicketAnswer
from shop_products.models import Product, ProductComment, ProductVisit, ProductAmazing
from shop_settings.models import SiteSetting
from shop_website.models import (
    HomePageSlider,
    HomePageBanners, Newsletters,
)
from tinakala.forms import NewslettersForm
from tinakala.utils import create_products_object_list, get_visitor_ip_address, django_process_background_tasks


def header(request, *args, **kwargs):
    site_logo: SiteSetting = SiteSetting.objects.all().first().logo

    categories_depth_one = SubCategoryParent.objects.filter(category__depth=1, category__is_active=True)
    categories_depth_two = SubCategoryParent.objects.filter(category__depth=2, sub_category__depth=3, sub_category__is_active=True) \
        .values_list('category', 'sub_category__title', 'sub_category__en_title', flat=False)

    categories_depth_three = []
    for category in categories_depth_two:
        categories_depth_three.append({
            'id': category[0],
            'title': category[1],
            'en_title': category[2],
        })

    cart = Cart(request)
    basket = {}
    cart_session = request.session.get('cart')
    basket['cart_length'] = len(list(cart_session))
    basket['nice_total_price'] = cart.get_nice_total_price()
    basket['products'] = []
    products_in_cart = Product.objects.filter(code__in=request.session.get('cart').keys())
    for product in products_in_cart:
        basket['products'].append({
            'code': product.code,
            'title': product.title,
            'avatar': product.avatar.url,
            'price': f'{cart_session[product.code]["price"]} تومان × {cart_session[product.code]["product_count"]}'
        })

    context = {
        'site_logo': site_logo,
        'categories_depth_one': categories_depth_one,
        'categories_depth_three': categories_depth_three,
        'basket': basket,
    }
    if request.user.is_authenticated:
        unread_message = UserTicketAnswer.objects.get_unread_answer_count(user=request.user)
        context['unread_message'] = unread_message

    return render(request, 'app_site/shared/SiteHeader.html', context)


def site_head_tags(request, *args, **kwargs):
    site_title: SiteSetting = SiteSetting.objects.all().first().title
    context = {
        'site_title': site_title
    }
    return render(request, 'app_site/shared/_SiteHeadTags.html', context)


def footer(request, *args, **kwargs):
    site_info: SiteSetting = SiteSetting.objects.all().first()
    # Register User For Newsletter
    newsletters_form = NewslettersForm(request.POST or None)
    if newsletters_form.is_valid():
        ip = get_visitor_ip_address(request=request)
        email = newsletters_form.cleaned_data.get('email')
        if ip['valid']:
            user = Newsletters.objects.filter(ip=ip['ip'], email=email).first()
            if not user:
                user = Newsletters.objects.create(ip=ip['ip'], email=email)
                user.save()
            messages.success(request, 'ایمیل شما با موفقیت ثبت شد!')

    context = {
        'site_info': site_info,
        'newsletters_form': newsletters_form,
    }
    return render(request, 'app_site/shared/SiteFooter.html', context)


def home_page(request, *args, **kwargs):
    slider = HomePageSlider.objects.all()
    brands = Brands.objects.all()[:10]
    group_next_slider_banners = HomePageBanners.objects.filter(position=1)
    group_below_most_sales_banners = HomePageBanners.objects.filter(position=2)

    # Suggested Products
    amazing_product = ProductAmazing.objects.all().values('product')
    objects: Product = Product.objects.filter(id__in=amazing_product)
    suggested_structured = create_products_object_list(objects, model=ProductComment, secondary_model=ProductAmazing)

    products = Product.objects.get_active_product()
    # Most Sales Products
    most_sales_structured = create_products_object_list(products.order_by('-total_sales')[:7], model=ProductComment, secondary_model=ProductAmazing)
    # Most Visited Products
    most_visited_structured = create_products_object_list(products.order_by('-total_visited')[:7], model=ProductComment, secondary_model=ProductAmazing)
    # Newest Products
    newest_structured = create_products_object_list(products[:7], model=ProductComment, secondary_model=ProductAmazing)
    # Advice Products
    if request.user.is_authenticated:
        favorites_scale = [item[0] for item in UserFavorite.objects.filter(user=request.user).values_list('product')]
        visits_scale = [item[0] for item in ProductVisit.objects.filter(user=request.user).values_list('product')]
        if favorites_scale:
            user_products = Product.objects.filter(id__in=favorites_scale)[:4]
        elif visits_scale:
            user_products = Product.objects.filter(id__in=visits_scale)[:4]
        else:
            user_products = products.order_by('-total_visited')[:4]
        advice = create_products_object_list(user_products, model=ProductComment)
    else:
        advice = most_visited_structured[:4]

    context = {
        'slider': slider,
        'brands': brands,
        'group_next_slider_banners': group_next_slider_banners[:2],
        'group_below_most_sales_banners': group_below_most_sales_banners[:2],
        'most_sales': most_sales_structured,
        'most_visited': most_visited_structured,
        'newest': newest_structured,
        'advice': advice,
        'suggested': suggested_structured,
    }
    return render(request, 'app_site/HomePage.html', context)
