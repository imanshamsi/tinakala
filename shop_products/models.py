import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_resized import ResizedImageField

from ckeditor_uploader.fields import RichTextUploadingField

from shop_categories.models import Category, Attribute, Brands
from tinakala.utils import upload_product_avatar, upload_product_media, get_filename_ext
from tinakala.utils.slug_generator import unique_slug_generator


class ProductManager(models.Manager):
    def get_active_product(self):
        return self.get_queryset().filter(is_active=True).order_by('-timestamp')

    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(en_title__icontains=query) |
            Q(category__title__icontains=query) |
            Q(category__en_title__icontains=query) |
            Q(brand__title__icontains=query) |
            Q(brand__en_title__icontains=query) |
            Q(review__icontains=query)
        )
        return self.get_queryset().filter(lookup, is_active=True).order_by('-timestamp').distinct()

    def get_products_by_category(self, category):
        return self.get_queryset().filter(category__en_title=category, is_active=True).order_by('-timestamp')


class Product(models.Model):
    PRODUCT_STATUS_CHOICES = (
        (False, 'اتمام موجودی کالا'),
        (True, 'موجودی فعال برای کالا'),
    )
    slug = models.SlugField(blank=True, unique=True, verbose_name='عنوان در آدرس')
    title = models.CharField(max_length=120, verbose_name='عنوان محصول به فارسی')
    en_title = models.CharField(max_length=120, null=True, blank=True, verbose_name='عنوان محصول به انگلیسی')
    code = models.CharField(max_length=12, null=True, blank=True, verbose_name='کد محصول')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت محصول')
    review = RichTextUploadingField(verbose_name='متن نقد و بررسی')
    avatar = ResizedImageField(size=[350, 350], quality=150, crop=['middle', 'center'], upload_to=upload_product_avatar,
                               verbose_name='عکس محصول')
    inventory = models.PositiveIntegerField(default=0, verbose_name='موجودی کالا')
    status = models.BooleanField(default=0, choices=PRODUCT_STATUS_CHOICES, verbose_name='وضعیت موجودی کالا')
    brand = models.ForeignKey(Brands, null=True, blank=True, on_delete=models.CASCADE, verbose_name='برند کالا')
    category = models.ManyToManyField(Category, verbose_name='مربوط به دسته')
    timestamp = models.DateTimeField(auto_now_add=True)
    total_sales = models.PositiveIntegerField(default=0, verbose_name='فروش کل محصول')
    total_visited = models.PositiveIntegerField(default=1, verbose_name='بازدید کل')
    is_active = models.BooleanField(default=True, verbose_name='فعال/ غیر فعال')

    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'مدیریت محصولات'

    def __str__(self):
        return self.title

    def get_nice_price(self):
        return f'{self.price:,}'

    def add_visit_count(self):
        self.total_visited += 1
        self.save()

    def subtraction_inventory_by_order(self, order_count):
        self.inventory -= order_count
        self.save()


@receiver(pre_save, sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.code:
        instance.code = f'tkp-{str(uuid.uuid4())[0:8]}'
    if instance.inventory <= 0:
        instance.status = False
    else:
        instance.status = True


class ProductGallery(models.Model):
    FILETYPE_CHOICES = (
        (1, 'عکس (png, jpg, ...)'),
        (2, 'ویدیو (mp4, ...)'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='مربوط به محصول')
    type = models.IntegerField(null=True, blank=True, choices=FILETYPE_CHOICES, verbose_name='نوع رسانه')
    media = models.FileField(upload_to=upload_product_media, verbose_name='رسانه مربوط به محصول')

    class Meta:
        verbose_name = 'رسانه های محصول'
        verbose_name_plural = 'گالری محصولات'

    def __str__(self):
        return f'{self.product.code}-{(self.media.size/1024):.2f} Kb'

    def get_file_type(self):
        name, ext = get_filename_ext(self.media.url)
        return f'{ext}'


@receiver(pre_save, sender=ProductGallery)
def product_gallery_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.media.size >= 52428800:
        raise PermissionDenied('حجم فایل بیش از مقدار مجاز است')
    name, ext = get_filename_ext(instance.media.url)
    if ext not in ['.png', '.PNG', '.jpg', '.JPG', '.mp4', '.MP4']:
        raise PermissionDenied('نوع فایل نامعتبر است')
    if ext in ['.png', '.PNG', '.jpg', '.JPG']:
        instance.type = 1
    if ext in ['.mp4', '.MP4']:
        instance.type = 2


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='مربوط به محصول')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='خصوصیت')
    value = models.CharField(max_length=200, verbose_name='مقدار خصوصیت')

    class Meta:
        verbose_name = 'خصوصیت محصول'
        verbose_name_plural = 'مدیریت خصوصیات محصولات'

    def __str__(self):
        return self.product.title


class ProductComment(models.Model):
    COMMENT_CHOICES = (
        (1, 'بسیار کم'),
        (2, 'کم'),
        (3, 'متوسط'),
        (4, 'زیاد'),
        (5, 'بسیار زیاد'),
    )
    ADVISED_CHOICES = (
        (True, 'این محصول را توصیه می کنم'),
        (False, 'این محصول را توصیه نمی کنم'),
    )
    user = models.ForeignKey(User, models.CASCADE, verbose_name='متعلق به کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='مربوط به محصول')
    title = models.CharField(max_length=120, verbose_name='عنوان نظر')
    comment = models.TextField(max_length=600, verbose_name='متن نظر')
    worth = models.IntegerField(default=3, choices=COMMENT_CHOICES, verbose_name='ارزش خرید')
    quality = models.IntegerField(default=3, choices=COMMENT_CHOICES, verbose_name='کیفیت ساخت')
    function = models.IntegerField(default=3, choices=COMMENT_CHOICES, verbose_name='عملکرد')
    advised = models.BooleanField(default=True, choices=ADVISED_CHOICES, verbose_name='توصیه به خرید میشود/نمی شود')
    timestamp = models.DateTimeField(default=datetime.now(), verbose_name='زمان ارسال')
    verified = models.BooleanField(default=False, verbose_name='تایید شده/نشده')
    promote = models.BooleanField(default=True, verbose_name='تایید توسط کاربر')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'مدیریت نظرات محصولات'

    def __str__(self):
        return f'{self.user.get_full_name()}'

    def get_product_code(self):
        return self.product.code

    def get_advised_text(self):
        if self.advised:
            return 'خرید این محصول را توصیه می کنم'
        else:
            return 'خرید این محصول را توصیه نمی کنم'


class ProductVisitManager(models.Manager):
    def get_product_visit(self, product, user):
        return self.get_queryset().filter(product=product, user=user).first()

    def get_product_visits_count(self, product):
        return self.get_queryset().filter(product=product).aggregate(Sum('count'))

    def get_product_by_user(self, user):
        return self.get_queryset().filter(user=user).order_by('-timestamp')


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='زمان بازدید')
    count = models.PositiveIntegerField(default=1, verbose_name='تعداد بازدید')

    objects = ProductVisitManager()

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'مدیریت بازدید محصولات'

    def __str__(self):
        return f'{self.user.get_full_name()}-{self.product.title}'

    def visited(self):
        self.count += 1
        self.save()


class ProductAmazing(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='محصول')
    discount = models.PositiveIntegerField(verbose_name='درصد تخفیف')

    class Meta:
        verbose_name = 'محصول شگفت انگیز'
        verbose_name_plural = 'مدیریت محصولات شگفت انگیز'

    def __str__(self):
        return f'{self.product.title} -> ({self.discount}%)'

    def get_price(self):
        return round(int(self.product.price) * ((100-self.discount)/100))

    def get_nice_price(self):
        return f'{self.get_price():,}'
