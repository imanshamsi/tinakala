from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ckeditor_uploader.fields import RichTextUploadingField
from django_resized import ResizedImageField

from tinakala.utils import unique_slug_generator, upload_blog_avatar


class BlogCategory(models.Model):
    fa_title = models.CharField(max_length=100, verbose_name='عنوان دسته')
    title = models.CharField(max_length=100, verbose_name='عنوان انگلیسی دسته')
    slug = models.SlugField(null=True, blank=True, verbose_name='عنوان در آدرس')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'مدیریت دسته بندی'

    def __str__(self):
        return self.fa_title


@receiver(pre_save, sender=BlogCategory)
def blog_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class BlogTag(models.Model):
    fa_title = models.CharField(max_length=100, verbose_name='عنوان تگ')
    title = models.CharField(max_length=100, verbose_name='عنوان انگلیسی تگ')
    slug = models.SlugField(null=True, blank=True, verbose_name='عنوان در آدرس')

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'مدیریت تگ ها'

    def __str__(self):
        return self.fa_title


@receiver(pre_save, sender=BlogTag)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class BlogManager(models.Manager):
    def get_blog_by_category_or_tag(self, query):
        lookup = (
                Q(categories__slug__iexact=query) |
                Q(tags__slug__iexact=query)
        )
        return self.get_queryset().filter(lookup).distinct()

    def get_blog_by_search(self, query):
        lookup = (
                Q(categories__fa_title__icontains=query) |
                Q(categories__title__icontains=query) |
                Q(tags__fa_title__icontains=query) |
                Q(tags__title__icontains=query) |
                Q(title__icontains=query) |
                Q(content__iexact=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
        )
        return self.get_queryset().filter(lookup).distinct()


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='نویسنده')
    title = models.CharField(max_length=150, verbose_name='عنوان مقاله')
    content = RichTextUploadingField(verbose_name='محتوای مقاله')
    avatar = ResizedImageField(size=[360, 225], quality=150, crop=['middle', 'center'], upload_to=upload_blog_avatar, verbose_name='آواتار مقاله')
    timestamp = models.DateTimeField(default=datetime.now(), verbose_name='زمان ارسال')
    categories = models.ManyToManyField(BlogCategory, verbose_name='مربوط به دسته بندی های')
    tags = models.ManyToManyField(BlogTag, verbose_name='مربوط به تگ های')

    objects = BlogManager()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مدیریت مقالات'

    def __str__(self):
        return f'{self.author.get_full_name()}-{self.title}'


class BlogViewManager(models.Manager):
    def blog_view_by_user(self, user, blog):
        return self.get_queryset().filter(user=user, blog=blog).first()

    def blog_view_counts(self, blog):
        return self.get_queryset().filter(blog=blog).count()


class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='بلاگ')
    user = models.CharField(max_length=15, verbose_name='آی پی بازدید کننده')

    objects = BlogViewManager()

    class Meta:
        verbose_name = 'ویوی بلاگ'
        verbose_name_plural = 'مدیریت ویو بلاگ ها'

    def __str__(self):
        return f'{self.blog}-{self.user}'
