from django.contrib import admin
from django.utils.html import format_html

from jalali_date.admin import ModelAdminJalaliMixin

from .models import (
    Product,
    ProductGallery,
    ProductAttribute,
    ProductComment,
    ProductVisit,
    ProductAmazing,
)


class ProductGalleryTabularInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductAttributeTabularInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'admin_get_product_avatar', '__str__', 'admin_get_product_price', 'is_active', ]
    search_fields = ['fa_title', 'en_title']
    list_per_page = 5
    inlines = [ProductGalleryTabularInline, ProductAttributeTabularInline]

    def admin_get_product_price(self, obj):
        return f'{obj.price:,} تومان'
    admin_get_product_price.short_description = 'قیمت'

    def admin_get_product_avatar(self, obj):
        return format_html(f'<img src="{obj.avatar.url}" width="64px" height="64px">')
    admin_get_product_avatar.short_description = 'آواتار محصول'


# @admin.register(ProductGallery)
# class ProductGalleryAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'admin_get_product_media_size', 'get_file_type']
#     list_filter = ['product']
#     list_per_page = 5
#
#     def admin_get_product_media_size(self, obj):
#         return f'{(obj.media.size/1024):.2f} Kb'
#     admin_get_product_media_size.short_description = 'اندازه رسانه'


# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'attribute', 'value']
#     list_filter = ['product']


@admin.register(ProductComment)
class ProductCommentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['__str__', 'get_product_code', 'advised', 'timestamp', 'verified', 'promote']
    list_editable = ['timestamp']
    list_filter = ['timestamp', 'verified', 'promote']


# @admin.register(ProductVisit)
# class ProductVisitAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
#     list_display = ['__str__', 'count', ]


@admin.register(ProductAmazing)
class ProductAmazingAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]
