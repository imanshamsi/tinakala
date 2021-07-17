from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django_resized import ResizedImageField

from tinakala.utils import (
    upload_home_page_slider,
    upload_home_page_banners,
)


class HomePageSlider(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان اسلاید')
    image = ResizedImageField(size=[873, 437], quality=150, crop=['middle', 'center'], upload_to=upload_home_page_slider, verbose_name='تصویر اسلاید')
    url = models.CharField(max_length=120, verbose_name='مربوط به صفحه')

    class Meta:
        verbose_name = 'اسلاید'
        verbose_name_plural = 'مدیریت اسلایدر صفحه اصلی'

    def __str__(self):
        return self.title


class HomePageBanners(models.Model):
    BANNER_CHOICES = (
        (1, 'کنار اسلایدر اصلی سایت'),
        (2, 'پایین پرفروش ترین ها'),
    )
    title = models.CharField(max_length=100, verbose_name='عنوان بنر')
    position = models.IntegerField(default=1, choices=BANNER_CHOICES, verbose_name='محل قرار گیری بنر')
    image = models.ImageField(upload_to=upload_home_page_banners, verbose_name='رسانه بنر')
    url = models.CharField(max_length=120, verbose_name='لینک صفحه بنر')

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'مدیریت بنر صفحه اصلی'

    def __str__(self):
        return self.title


class Newsletters(models.Model):
    ip = models.CharField(max_length=15, verbose_name='آی پی کاربر')
    email = models.EmailField(verbose_name='ایمیل کاربر')

    class Meta:
        verbose_name = 'کاربر خبرنامه'
        verbose_name_plural = 'مدیریت کاربران خبرنامه'

    def __str__(self):
        return f'IP {self.ip}'


class NewslettersMessage(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان خبر')
    message = models.TextField(verbose_name='متن خبرنامه')
    html = models.TextField(null=True, blank=True, verbose_name='محتوای html')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='زمان خبر')

    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'مدیریت خبرنامه'

    def __str__(self):
        return self.title
