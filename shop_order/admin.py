from django.contrib import admin
from jalali_date import date2jalali

from shop_order.models import *


class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class InvoiceTabularInline(admin.TabularInline):
    model = Invoice
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_date', 'order_code', 'is_paid']
    list_filter = ['is_paid']
    inlines = [OrderItemTabularInline, InvoiceTabularInline]

    def admin_get_date(self, obj):
        return date2jalali(obj.order_date).strftime('%Y/%m/%d')

    admin_get_date.short_description = 'تاریح سبد خرید'


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'product']


class TransactionTabularInline(admin.TabularInline):
    model = Transaction
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'admin_get_date', 'authority']
    inlines = [TransactionTabularInline]

    def admin_get_date(self, obj):
        return date2jalali(obj.invoice_date).strftime('%Y/%m/%d')

    admin_get_date.short_description = 'تاریح صورت حساب'


# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'admin_get_date', 'amount', 'status']
#     list_filter = ['status']
#
#     def admin_get_date(self, obj):
#         return date2jalali(obj.transaction_date).strftime('%Y/%m/%d')
#
#     admin_get_date.short_description = 'تاریح تراکنش'
