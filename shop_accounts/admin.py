from django.contrib import admin
from django.utils.html import format_html


from jalali_date import date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


from .models import (
    UserProfile,
    UserAddress,
    UserFavorite, UserCommentVote,
)


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_avatar', 'gender', 'phone', 'phone_verify', 'otp', 'admin_get_birthday',
                    'national_code', 'done', 'point']

    def admin_get_birthday(self, obj):
        return date2jalali(obj.birth_day).strftime('%Y/%m/%d')

    admin_get_birthday.short_description = 'تاریخ تولد'

    def admin_get_avatar(self, obj):
        if obj.avatar:
            return format_html(f'<img src="{obj.avatar.url}" width="64px" height="64px">')
        else:
            return format_html('<img src="/site_static/admin/img/icon-no.svg" alt="False">')
    admin_get_avatar.short_description = 'آواتار کاربر'


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_receiver_name', 'state', 'city', 'address', 'postal_code', 'plaque']

    def admin_get_receiver_name(self, obj):
        return f'آدرس متعلق به {obj.fullname} به شماره همراه {obj.phone}'
    admin_get_receiver_name.short_description = 'آدرس متعلق به'


# @admin.register(UserFavorite)
# class UserFavoriteAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'admin_get_favorite_products']
#
#     def admin_get_favorite_products(self, obj):
#         products = obj.product.all()
#         style = 'font-size:14px;'
#         represent = ''
#         for product in products:
#             represent += f'<a style="{style}" href="#">{product}</a><br><br><hr>'
#         return format_html(represent)
#     admin_get_favorite_products.short_description = 'محصولات مورد علاقه'


# @admin.register(UserCommentVote)
# class UserCommentVoteAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'admin_get_comment_vote', 'admin_get_timestamp']
#
#     def admin_get_comment_vote(self, obj):
#         vote = 'می پسندد' if obj.vote else 'نمی پسندد'
#         return vote
#     admin_get_comment_vote.short_description = 'امتیاز به نظر کاربر'
#
#     def admin_get_timestamp(self, obj):
#         return date2jalali(obj.timestamp).strftime('%Y/%m/%d')
#
#     admin_get_timestamp.short_description = 'تاریخ ارسال نظر'
