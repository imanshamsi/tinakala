from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_resized.forms import ResizedImageField

from tinakala.utils import upload_brand_logo


class CategoryQuerySet(models.query.QuerySet):
    def active_category(self):
        return self.filter(is_active=True)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active_category()


class Category(models.Model):
    DEPTH_CHOICES = (
        (1, 'دسته بندی سطح 1'),
        (2, 'دسته بندی سطح 2'),
        (3, 'دسته بندی سطح 3'),
    )
    title = models.CharField(max_length=40, verbose_name='عنوان دسته')
    en_title = models.CharField(max_length=40, null=True, blank=True, verbose_name='عنوان انگلیسی دسته')
    depth = models.IntegerField(default=1, choices=DEPTH_CHOICES, verbose_name='دسته مربوط به سطح')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال')

    objects = CategoryManager()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'مدیریت دسته بندی'

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def category_pre_save_title(sender, instance, *args, **kwargs):
    if instance.en_title and 'category' in instance.en_title:
        en_title = instance.en_title.replace('category', '').replace('-', '')
        instance.en_title = f'category-{en_title.replace(" ", "-")}'
    else:
        instance.en_title = f'category-{instance.en_title.replace(" ", "-")}'


class SubCategoryParent(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته والد')
    sub_category = models.ManyToManyField(Category, blank=True, related_name='sub_category', verbose_name='دسته فرزند')

    class Meta:
        verbose_name = 'زیر دسته'
        verbose_name_plural = 'مدیریت ارث بری دسته'

    def __str__(self):
        return self.category.title


class AttributeGroup(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='مربوط به دسته')
    title = models.CharField(max_length=40, verbose_name='عنوان خصوصیت دسته')

    class Meta:
        verbose_name = 'گروه خصوصیت'
        verbose_name_plural = 'مدیریت گروه خصوصیت'

    def __str__(self):
        return f'{self.category.title}/{self.title}'


class Attribute(models.Model):
    attr_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, verbose_name='مربوط به دسته خصوصیت')
    title = models.CharField(max_length=40, verbose_name='عنوان خصوصیت')

    class Meta:
        verbose_name = 'خصوصیت'
        verbose_name_plural = 'مدیریت خصوصیت'

    def __str__(self):
        return f'{self.attr_group.category.title}/{self.attr_group.title}/{self.title}'


class Brands(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان برند')
    en_title = models.CharField(max_length=120, verbose_name='عنوان انگلیسی برند')
    avatar = ResizedImageField(size=[205, 205], quality=150, upload_to=upload_brand_logo, crop=['middle', 'center'], verbose_name='لوگوی برند')
    categories = models.ManyToManyField(Category, verbose_name='مربوط به دسته های')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'مدیریت برندها'

    def __str__(self):
        return self.title
