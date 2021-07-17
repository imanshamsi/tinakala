from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    fullname = models.CharField(max_length=40, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره همراه')
    email = models.EmailField(verbose_name='ایمیل')
    title = models.CharField(max_length=60, verbose_name='عنوان')
    content = models.TextField(verbose_name='متن پیام')
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد')
    read = models.BooleanField(default=False, verbose_name='خوانده شده/نشده')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'مدیریت پیام ها'

    def __str__(self):
        return self.title


class UserTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='تیکت مربوط به کاربر')
    title = models.CharField(max_length=200, verbose_name='عنوان تیکت')
    question = RichTextUploadingField(verbose_name='متن تیکت')
    timestamp = models.DateTimeField(default=datetime.now(), verbose_name='زمان ایجاد تیکت')
    active = models.BooleanField(default=True, verbose_name='تیکت فعال/غیرفعال')

    class Meta:
        verbose_name = 'تیک کاربر'
        verbose_name_plural = 'مدیریت تیکت کاربران'

    def __str__(self):
        return f'{self.user.get_full_name()}-{self.title}'


class UserTicketAnswerManager(models.Manager):
    def get_ticket_answers(self, ticket):
        return self.get_queryset().filter(ticket=ticket).order_by('timestamp')

    def get_unread_answer_count(self, user, ticket=None):
        if ticket:
            return self.get_queryset().filter(ticket=ticket, ticket__user=user, read=False).count()
        else:
            return self.get_queryset().filter(ticket__user=user, read=False).count()


def set_read_mark_for_answers(queryset):
    for answer in queryset:
        answer.read = True
        answer.save()


class UserTicketAnswer(models.Model):
    ticket = models.ForeignKey(UserTicket, on_delete=models.CASCADE, verbose_name='مربوط به تیکت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر پاسخ دهنده')
    answer = RichTextUploadingField(verbose_name='پاسخ تیکت')
    timestamp = models.DateTimeField(default=datetime.now(), verbose_name='زمان پاسخ تیکت')
    read = models.BooleanField(default=False, verbose_name='خوانده شده/نشده')

    objects = UserTicketAnswerManager()

    class Meta:
        verbose_name = 'پاسخ تیکت'
        verbose_name_plural = 'مدیریت پاسخ تیکت ها'

    def __str__(self):
        return f'{self.ticket.title}-{self.user.get_full_name()}'

    def read_ticket_answer(self):
        self.read = True
        self.save()
