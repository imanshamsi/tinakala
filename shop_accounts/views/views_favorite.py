"""
shop_accounts -> views -> user favorite methods
"""
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from pure_pagination import Paginator, PageNotAnInteger

from shop_accounts.models import UserProfile, UserFavorite
from shop_products.models import Product, ProductComment
from tinakala.utils import profile_completion_required, create_products_object_list


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_favorite(request, *args, **kwargs):
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    favorites: UserFavorite = UserFavorite.objects.filter(user=request.user, product__is_active=True).first()
    favorites = create_products_object_list(favorites.product.all(), model=ProductComment) if favorites else []

    context = {
        'favorites': Paginator(favorites, per_page=10, request=request).page(page),
    }
    return render(request, 'accounts/SiteUserFavorite.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_favorite_add(request, *args, **kwargs):
    slug = kwargs['slug']
    product = Product.objects.filter(slug=slug).first()
    if product:
        user_favorite_object: UserFavorite = UserFavorite.objects.filter(user=request.user).first()
        if user_favorite_object:
            user_favorite_object.product.add(product)
            user_favorite_object.save()
            message = 'این کالا با موفقیت به لیست علاقه مندی شما اضافه شد.'
        else:
            user_favorite_object = UserFavorite.objects.create(user=request.user)
            user_favorite_object.product.add(product)
            user_favorite_object.save()
            message = 'این کالا با موفقیت به لیست علاقه مندی شما اضافه شد.'
        result = True
    else:
        result = False
        message = f'کالایی با عنوان <<{slug}>> یافت نشد.'
    return JsonResponse([message, result], safe=False)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_favorite_delete(request, *args, **kwargs):
    slug = kwargs['slug']
    favorite: UserFavorite = get_object_or_404(UserFavorite, user=request.user)
    product = get_object_or_404(Product, slug=slug)
    if favorite:
        favorite.product.remove(product)
        favorite.save()
        messages.success(request, f'کالای <<{product.title}>> از لیست علاقه مندی با موفقیت حذف گردید.')
    else:
        messages.error(request, f'کالایی با عنوان {slug} در لیست علاقه مندی شما موجود نمی باشد.')
    return redirect('auth:user-favorite')
