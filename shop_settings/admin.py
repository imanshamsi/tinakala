from django.contrib import admin
from django.utils.html import format_html
from jalali_date import date2jalali

from jalali_date.admin import ModelAdminJalaliMixin

from shop_settings.models import (
    State,
    City,
    SiteSetting,
)
admin.site.site_header = 'ادمین فروشگاه اینترنتی تیناکالا'
admin.site.site_title = 'فروشگاه اینترنتی تیناکالا'
admin.site.index_title = 'پنل ادمین'


class CityTabularInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(State)
class StateManagementAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    inlines = [CityTabularInline]


# @admin.register(City)
# class CityManagementAdmin(admin.ModelAdmin):
#     list_display = ['state', '__str__']
#     list_filter = ['state']


@admin.register(SiteSetting)
class SiteSettingAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_site_logo', 'admin_get_site_birth']

    def admin_get_site_birth(self, obj):
        return date2jalali(obj.site_birth).strftime('%Y/%m/%d')

    admin_get_site_birth.short_description = 'تولد سایت'

    def admin_get_site_logo(self, obj):
        if obj.logo:
            return format_html(f'<img src="{obj.logo.url}" width="128px" height="36px">')
        else:
            return format_html('<img src="/site_static/app_site/img/logo.png" alt="False">')
    admin_get_site_logo.short_description = 'لوگوی سایت'
