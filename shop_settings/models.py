from django.db import models

from django_resized import ResizedImageField
from ckeditor_uploader.fields import RichTextUploadingField

from tinakala.utils import upload_site_logo, upload_site_certificate


class State(models.Model):
    state = models.CharField(max_length=20, verbose_name='نام استان')

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'مدیریت استان ها'

    def __str__(self):
        return self.state


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='مربوط به استان')
    city = models.CharField(max_length=20, verbose_name='نام شهر')

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'مدیریت شهرها'

    def __str__(self):
        return self.city


class SiteSetting(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان سایت')
    logo = ResizedImageField(size=[128, 36], quality=150, crop=['middle', 'center'], upload_to=upload_site_logo,
                             null=True, blank=True, verbose_name='لوگوی سایت')
    site_birth = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد سایت')
    abstract = models.TextField(max_length=500, verbose_name='خلاصه معرفی')

    copyright = models.CharField(max_length=100, verbose_name='متن کپی رایت')
    copyright_access = models.CharField(max_length=200, verbose_name='اجازه کپی رایت مطالب')

    privacy_rules = RichTextUploadingField(null=True, blank=True, verbose_name='متن حریم خصوصی')

    link_twitter = models.CharField(max_length=100, null=True, blank=True, verbose_name='لینک تویتر')
    link_telegram = models.CharField(max_length=100, null=True, blank=True, verbose_name='لینک تلگرام')
    link_instagram = models.CharField(max_length=100, null=True, blank=True, verbose_name='لینک اینستگرام')
    link_facebook = models.CharField(max_length=100, null=True, blank=True, verbose_name='لینک فیسبوک')

    samandehi = ResizedImageField(size=[145, 145], quality=150, crop=['middle', 'center'],
                                  upload_to=upload_site_certificate, null=True, blank=True,
                                  verbose_name='نماد سازمان ساماندهی')
    link_samandehi = models.CharField(max_length=90, null=True, blank=True, verbose_name='لینک سازمان ساماندهی')
    electronic = ResizedImageField(size=[145, 145], quality=150, crop=['middle', 'center'],
                                   upload_to=upload_site_certificate, null=True, blank=True,
                                   verbose_name='نماد سازمان تجارت الکترونیک')
    link_electronic = models.CharField(max_length=90, null=True, blank=True, verbose_name='لینک سازمان تجارت الکترونیک')

    sms_message = models.CharField(max_length=120, verbose_name='متن پیامک فعال سازی')

    class Meta:
        verbose_name = 'تنظیمات وب اپلیکیشن'
        verbose_name_plural = 'تنظیمات وب اپلیکیشن'

    def __str__(self):
        return self.title
