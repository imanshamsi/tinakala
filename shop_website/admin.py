from django.contrib import admin
from django.utils.html import format_html

from jalali_date import date2jalali

from shop_website.models import HomePageSlider, HomePageBanners, Newsletters, NewslettersMessage
from tinakala.utils import admin_sent_news_mail


@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_slide', 'url']
    list_per_page = 5

    def admin_get_slide(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="350px" height="175px">')
    admin_get_slide.short_description = 'تصویر اسلاید'


@admin.register(HomePageBanners)
class HomePageBannersAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_banner', 'position', 'url']
    list_editable = ['position']
    list_per_page = 5

    def admin_get_banner(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="214px" height="107px">')
    admin_get_banner.short_description = 'تصویر بنر'


# @admin.register(Newsletters)
# class NewslettersAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'email', ]
#     list_per_page = 10


@admin.register(NewslettersMessage)
class NewslettersMessageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_date', ]
    list_per_page = 5
    actions = ['admin_send_emails']

    def admin_send_emails(self, request, queryset):
        for news in queryset:
            users = [email[0] for email in list(Newsletters.objects.all().values_list('email'))]
            subject = news.title
            content = news.message
            html = news.html
            admin_sent_news_mail(subject=subject, content=content, html=html, users=users)
        self.message_user(request=request, message='خبر با موفقیت برای کاربران ارسال شد!')
    admin_send_emails.short_description = 'ارسال خبر برای تمام کاربران'

    def admin_get_date(self, obj):
        return date2jalali(obj.timestamp).strftime('%Y/%m/%d')
    admin_get_date.short_description = 'تاریح خبر'
