from django.contrib import messages
from django.db.models import Avg, Max, Min
from django.shortcuts import render, get_object_or_404, redirect

from pure_pagination import Paginator, PageNotAnInteger

from shop_accounts.models import UserFavorite
from shop_cart.forms import AddProductToCart
from shop_categories.models import (
    SubCategoryParent,
    Category, Brands,
)
from shop_order.models import OrderItem
from shop_products.forms import (
    ProductSendCommentsForm,
    ProductByCategoryBrandFilterForm,
)
from shop_products.models import (
    Product,
    ProductGallery,
    ProductAttribute,
    ProductComment,
    ProductVisit, ProductAmazing,
)
from tinakala.utils import (
    percent_2_text,
    check_vote,
    create_products_object_list,
    sort_product_by_filter,
    product_by_filter,
)
from tinakala.utils.category_methods import (
    side_bar_categories_menu,
    get_most_category,
)


def side_bar_filter_form(request, searched_category, objects):
    form = []
    if objects:
        form = ProductByCategoryBrandFilterForm(request.GET or None, category=searched_category, initial={
            'price_start': objects.aggregate(Min('price'))['price__min'],
            'price_end': objects.aggregate(Max('price'))['price__max'],
        })
    return form


def search_products_view(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    # get value of q for search
    query = request.GET.get('q')
    objects = Product.objects.search(query) if query is not None else Product.objects.get_active_product()
    searched_category = get_most_category(objects, Category)

    form = side_bar_filter_form(request, searched_category, objects)
    filtered_object = product_by_filter(request, objects)
    sorted_products = sort_product_by_filter(request, filtered_object)
    structured_products = create_products_object_list(sorted_products, model=ProductComment, secondary_model=ProductAmazing)
    paginated_products = Paginator(structured_products, request=request, per_page=8).page(page)

    parent, child = side_bar_categories_menu(category=searched_category, model=SubCategoryParent)

    context = {
        'form': form,
        'object_list': paginated_products,
        'parent': parent,
        'child': child,
    }
    return render(request, 'products/SiteProducts.html', context)


def search_product_by_category_view(request, category):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    searched_category = get_object_or_404(Category, en_title=category)
    objects: Product = Product.objects.get_products_by_category(category=category)

    form = side_bar_filter_form(request, searched_category, objects)
    filtered_object = product_by_filter(request, objects)
    sorted_products = sort_product_by_filter(request, filtered_object)
    structured_products = create_products_object_list(sorted_products, model=ProductComment, secondary_model=ProductAmazing)
    paginated_products = Paginator(structured_products, request=request, per_page=8).page(page)

    parent, child = side_bar_categories_menu(category=searched_category, model=SubCategoryParent)

    context = {
        'form': form,
        'object_list': paginated_products,
        'parent': parent,
        'child': child,
    }
    return render(request, 'products/SiteProducts.html', context)


def get_product_by_brand_view(request, brand):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    searched_brand = get_object_or_404(Brands, en_title=brand)
    objects: Product = Product.objects.filter(brand=searched_brand)
    sorted_products = sort_product_by_filter(request, objects)
    structured_products = create_products_object_list(sorted_products, model=ProductComment, secondary_model=ProductAmazing)
    paginated_products = Paginator(structured_products, request=request, per_page=16).page(page)

    context = {
        'brand': searched_brand,
        'object_list': paginated_products,
    }
    return render(request, 'products/SiteProductsByBrand.html', context)


def get_product_amazing(request):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    amazing_product = ProductAmazing.objects.all().values('product')
    objects: Product = Product.objects.filter(id__in=amazing_product)
    sorted_products = sort_product_by_filter(request, objects)
    structured_products = create_products_object_list(sorted_products, model=ProductComment, secondary_model=ProductAmazing)
    paginated_products = Paginator(structured_products, request=request, per_page=16).page(page)

    context = {
        'object_list': paginated_products,
    }
    return render(request, 'products/SiteProductSuggested.html', context)


def detail_product_view(request, *args, **kwargs):
    # Get product, amazing, categories, add total visit
    product_code = kwargs['product_code']
    product = get_object_or_404(Product, code=product_code)
    amazing = ProductAmazing.objects.filter(product=product).first()
    product.add_visit_count()
    categories = product.category.all().order_by('depth')
    # Set product, visit count for authenticated user
    if request.user.is_authenticated:
        visit: ProductVisit = ProductVisit.objects.get_product_visit(product=product, user=request.user)
        if visit:
            visit.visited()
        else:
            ProductVisit.objects.create(product=product, user=request.user)
    # Get product media
    product_media = ProductGallery.objects.filter(product=product)
    # Check product is favorite for authenticated user or not
    is_favorite = UserFavorite.objects.filter(product=product, user=request.user).exists() \
        if request.user.is_authenticated else False
    # Get product attributes
    product_attributes = ProductAttribute.objects.filter(product=product)
    attr_group_keys = []
    attr_attribute_keys = []
    for item in product_attributes.values_list('attribute__attr_group__title', 'attribute__title', 'value'):
        attr_group_keys.append(item[0])
        attr_attribute_keys.append({
            'group': item[0],
            'key': item[1],
            'value': item[2],
        })
    attr_group_keys = list(dict.fromkeys(attr_group_keys))
    # Get page number from request.GET
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    # Get products comments
    comments = []
    for comment in ProductComment.objects.filter(product=product, verified=True):
        is_buyer = OrderItem.objects.filter(product=product, order__customer=comment.user, order__is_paid=True).exists()
        comments.append({
            'id': comment.id,
            'title': comment.title,
            'comment': comment.comment,
            'advised': comment.advised,
            'get_advised_text': comment.get_advised_text(),
            'user_fullname': comment.user.get_full_name(),
            'timestamp': comment.timestamp,
            'is_buyer': is_buyer,
            'positive': comment.usercommentvote_set.filter(vote=True).count(),
            'negative': comment.usercommentvote_set.filter(vote=False).count(),
        })
    paginated_comments = Paginator(comments, request=request, per_page=5).page(page)
    # Create comment send form, Add new comment
    send_comment_form = ProductSendCommentsForm(request.POST or None)
    if send_comment_form.is_valid():
        comment = ProductComment.objects.create(
            user=request.user,
            product=product,
            title=send_comment_form.cleaned_data.get('title'),
            comment=send_comment_form.cleaned_data.get('comment'),
            advised=send_comment_form.cleaned_data.get('advised'),
            worth=send_comment_form.cleaned_data.get('worth'),
            quality=send_comment_form.cleaned_data.get('quality'),
            function=send_comment_form.cleaned_data.get('function'),
        )
        comment.save()
        messages.success(request, 'نظر شما با موفقیت ثبت شد. منتظر تایید مدیریت باشید.')
        return redirect('auth:user-comment')
    # Calculate point of product
    product_state = ProductComment.objects.filter(product=product)
    product_param = [
        check_vote(product_state.aggregate(Avg('worth'))['worth__avg']) * 20,
        check_vote(product_state.aggregate(Avg('quality'))['quality__avg']) * 20,
        check_vote(product_state.aggregate(Avg('function'))['function__avg']) * 20,
    ]
    param_avg = {
        'worth': {
            'value': round(product_param[0], 1),
            'stage': percent_2_text(product_param[0])
        },
        'quality': {
            'value': round(product_param[1], 1),
            'stage': percent_2_text(product_param[1])
        },
        'function': {
            'value': round(product_param[2], 1),
            'stage': percent_2_text(product_param[2])
        },
    }
    total_avg = ProductComment.objects.filter(product=product).values_list('worth', 'quality', 'function')
    try:
        total_avg = round(sum(sum(item) for item in total_avg)/(3*len(total_avg)), 1)
    except ZeroDivisionError:
        total_avg = 0
    # Create add to order form
    cart_add_product_form = AddProductToCart(inventory=product.inventory)

    context = {
        'product': product,
        'amazing': amazing if amazing else None,
        'categories': categories,
        'cart_add_product_form': cart_add_product_form,

        'product_media_images': product_media.filter(type__exact=1),
        'product_media_videos': product_media.filter(type__exact=2),

        'attr_group_keys': attr_group_keys,
        'attr_attribute_keys': attr_attribute_keys,

        'object_list': paginated_comments,
        'number_of_comments': len(comments),

        'comment_form': send_comment_form,

        'is_favorite': is_favorite,

        'param_avg': param_avg,
        'total_avg': total_avg,
    }
    return render(request, 'products/SiteSingleProduct.html', context)
