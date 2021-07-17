from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    SubCategoryParent,
    AttributeGroup,
    Attribute,
    Brands,
)


class SubCategoryParentTabularInline(admin.TabularInline):
    model = SubCategoryParent
    max_num = 1


class AttributeGroupTabularInline(admin.TabularInline):
    model = AttributeGroup
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'en_title', 'depth', 'is_active', ]
    list_editable = ['en_title']
    list_filter = ['depth', ]
    list_display_links = ['__str__']
    inlines = [SubCategoryParentTabularInline, AttributeGroupTabularInline]


# @admin.register(SubCategoryParent)
# class SubCategoryParentAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'admin_get_sub_category', ]
#
#     def admin_get_sub_category(self, obj):
#         category = obj.category
#         sub_category = obj.sub_category.filter(depth=category.depth + 1)
#         style = 'font-size:14px;'
#         represent = ''
#         for sub in sub_category:
#             represent += f'<a style="{style}" href="#">{sub}</a><br><br><hr>'
#         return format_html(represent)
#     admin_get_sub_category.short_description = 'زیر دسته ها'


class AttributeTabularInline(admin.TabularInline):
    model = Attribute
    extra = 1


@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', ]
    inlines = [AttributeTabularInline]


# @admin.register(Attribute)
# class AttributeAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'title', ]


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_categories', 'admin_get_brands', ]

    def admin_get_brands(self, obj):
        if obj.avatar:
            return format_html(f'<img src="{obj.avatar.url}" width="150px" height="150px">')
        else:
            return 'Not Found'
    admin_get_brands.short_description = 'تصویر برند'

    def admin_get_categories(self, obj):
        categories = obj.categories
        style = 'font-size:14px;'
        represent = ''
        for category in categories.all().order_by('depth'):
            represent += f'<a style="{style}" href="#">{category}</a><br><br><hr>'
        return format_html(represent)
    admin_get_categories.short_description = 'مربوط به دسته های'
