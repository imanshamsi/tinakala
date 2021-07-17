from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin

from .models import (
    BlogCategory,
    BlogTag,
    Blog,
    BlogView
)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'slug']
    list_per_page = 5


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'slug']
    list_per_page = 5


@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['__str__', 'timestamp', ]
    list_editable = ['timestamp']
    list_per_page = 5


# @admin.register(BlogView)
# class BlogViewAdmin(admin.ModelAdmin):
#     list_display = ['__str__', ]
#     list_per_page = 5
