import os
from random import randint


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_user_avatar(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'user-{randint(1000, 9999)}-{instance.user.id}{ext}'
    return f'user/avatar/{final_name}'


def upload_site_logo(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'logo{ext}'
    return f'site/{final_name}'


def upload_site_certificate(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{randint(1000, 9999)}-certificate{ext}'
    return f'site/{final_name}'


def upload_product_avatar(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.slug}{ext}'
    return f'products/{final_name}'


def upload_product_media(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.product.slug}-{randint(1000, 9999)}{ext}'
    return f'products/gallery/{instance.product.slug}/{final_name}'


def upload_brand_logo(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.en_title}-{randint(1000, 9999)}{ext}'
    return f'brands/{instance.en_title}/{final_name}'


def upload_home_page_slider(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.title}-{randint(1000, 9999)}{ext}'
    return f'site/slider/home_page/{final_name}'


def upload_home_page_banners(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.title}-{randint(1000, 9999)}{ext}'
    return f'site/slider/banners/{final_name}'


def upload_blog_avatar(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.title}-{randint(1000, 9999)}{ext}'
    return f'site/blog/{final_name}'
