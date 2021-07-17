from django.http import Http404


def boolean_star(iterate):
    iterate = [True] * int(iterate)
    iterate += [False] * (5 - len(iterate))
    return iterate


def get_total_average(iterate):
    sum_iter = sum(sum(item) for item in iterate)
    if len(iterate):
        _ = round(sum_iter/(3 * len(iterate)), 0)
    else:
        _ = 0
    return boolean_star(_)


def create_products_object_list(objects, model, secondary_model=False):
    amazing = []
    products = []
    for product in objects:
        total_avg = model.objects.filter(product=product).values_list('worth', 'quality', 'function')
        if secondary_model:
            amazing = secondary_model.objects.filter(product=product).first()
        products.append({
            'title': product.title,
            'code': product.code,
            'slug': product.slug,
            'status': product.status,
            'inventory': product.inventory,
            'avatar': product.avatar.url,
            'price': product.get_nice_price(),
            'get_nice_price': product.get_nice_price() if not amazing else amazing.get_nice_price(),
            'avg': get_total_average(total_avg),
            'amazing': amazing,
        })
    return products


def product_by_filter(request, objects):
    filter_attr = request.GET
    brands = filter_attr.getlist('brands')
    start_price = filter_attr.get('price_start')
    end_price = filter_attr.get('price_end')
    is_exist = filter_attr.get('is_exist')
    if brands:
        objects = objects.filter(brand__in=[int(item) for item in brands])
    if start_price and end_price:
        objects = objects.filter(price__gte=start_price, price__lte=end_price)
    if is_exist:
        objects = objects.filter(status=True)
    return objects


def sort_product_by_filter(request, objects):
    product_sort_filter = request.GET.get('sorted')
    if product_sort_filter == 'newest' or product_sort_filter is None:
        objects = objects.order_by('-timestamp')
    elif product_sort_filter == 'expensive':
        objects = objects.order_by('-price')
    elif product_sort_filter == 'cheapest':
        objects = objects.order_by('price')
    elif product_sort_filter == 'most_visited':
        objects = objects.order_by('-total_visited')
    elif product_sort_filter == 'most_sales':
        objects = objects.order_by('-total_sales')
    else:
        raise Http404('صفحه مورد نظر یافت نشد')
    return objects
