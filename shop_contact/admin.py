from django.contrib import admin, messages
from django.utils.translation import ngettext
from jalali_date import date2jalali

from jalali_date.admin import ModelAdminJalaliMixin

from .models import Ticket, UserTicket, UserTicketAnswer


@admin.register(Ticket)
class TicketAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'email', 'admin_get_date_of_message', 'read', ]
    list_filter = ['created_at', ]
    actions = ['mark_as_read']

    def admin_get_date_of_message(self, obj):
        return date2jalali(obj.created_at).strftime('%Y/%m/%d')
    admin_get_date_of_message.short_description = 'تاریح پیام'

    def mark_as_read(self, request, queryset):
        read = queryset.update(read=True)
        self.message_user(request, ngettext(
            '%d پیام was successfully marked as خوانده شده',
            '%d پیام was successfully marked as خوانده شده',
            read,
        ) % read, messages.SUCCESS)
    mark_as_read.short_description = 'انتخاب به عنوان خوانده شده'


class UserTicketAnswerStackedInline(admin.StackedInline):
    model = UserTicketAnswer
    extra = 1


@admin.register(UserTicket)
class UserTicketAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'admin_get_date_of_ticket', ]
    list_filter = ['timestamp', ]
    inlines = [UserTicketAnswerStackedInline]

    def admin_get_date_of_ticket(self, obj):
        return date2jalali(obj.timestamp).strftime('%y/%m/%d _ %H:%M:%S')
    admin_get_date_of_ticket.short_description = 'تاریح تیکت'


# @admin.register(UserTicketAnswer)
# class UserTicketAnswerAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
#     list_display = ['__str__', 'read', 'admin_get_date_of_ticket_answer', ]
#     list_filter = ['timestamp', ]
#
#     def admin_get_date_of_ticket_answer(self, obj):
#         return date2jalali(obj.timestamp).strftime('%y/%m/%d _ %H:%M:%S')
#     admin_get_date_of_ticket_answer.short_description = 'تاریح تیکت'
