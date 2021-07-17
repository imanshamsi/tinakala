from django.contrib.auth.models import User
from django.db import models

from django_resized import ResizedImageField

from shop_products.models import Product, ProductComment
from shop_settings.models import State, City
from tinakala.utils import upload_user_avatar


class UserProfile(models.Model):
    """
    User Profile Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='حساب کاربری')
    avatar = ResizedImageField(size=[128, 128], quality=75, crop=['middle', 'center'], upload_to=upload_user_avatar,
                               null=True, blank=True, verbose_name='آواتار کاربر')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره همراه')
    phone_verify = models.BooleanField(default=0, verbose_name='تایید شماره همراه')
    otp = models.CharField(max_length=5,  null=True, blank=True, verbose_name='کد تایید موبایل')
    otp_generated_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ otp')
    GENDER_CHOICES = (
        (1, 'مرد'),
        (2, 'زن'),
    )
    gender = models.IntegerField(default=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='جنسیت')
    national_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد ملی')
    birth_day = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    done = models.BooleanField(default=0, verbose_name='تکمیل پروفایل')
    point = models.PositiveIntegerField(default=0, verbose_name='امتیاز کاربر')

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

    def get_full_name(self):
        return User.get_full_name(self.user)

    def __str__(self):
        return User.get_full_name(self.user)

    def add_point(self, number):
        self.point += number
        self.save()


class UserAddress(models.Model):
    """
        User Address Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='برای حساب کاربری')
    fullname = models.CharField(max_length=40, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=11, verbose_name='شماره همراه')
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='استان')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='شهر')
    address = models.TextField(max_length=500, verbose_name='آدرس')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    plaque = models.CharField(max_length=10, verbose_name='پلاک منزل')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'آدرس های کاربر'
        verbose_name_plural = 'آدرس های کاربران'

    def __str__(self):
        return f'{self.state} / {self.city} / {self.fullname}'


class UserFavorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ManyToManyField(Product, blank=True, verbose_name='محصولات مورد علاقه')

    class Meta:
        verbose_name = 'محصول مورد علاقه'
        verbose_name_plural = 'مدیریت علاقه مندی ها'

    def __str__(self):
        return self.user.get_full_name()


class UserCommentVote(models.Model):
    VOTE_CHOICES = (
        (True, 'می پسندم'),
        (False, 'نمی پسندم'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر ارسال کننده')
    comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE, verbose_name='مربوط به کامنت')
    vote = models.BooleanField(choices=VOTE_CHOICES, verbose_name='امتیاز شما')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت امتیاز')

    class Meta:
        verbose_name = 'امتیاز نظر'
        verbose_name_plural = 'مدیریت امتیاز نظرات'

    def __str__(self):
        return f'امتیاز کاربر <<{self.user.get_full_name()}>> به کامنت کاربر <<{self.comment.user.get_full_name()}>>'

    def positive_comment_vote(self):
        self.vote = True
        self.save()

    def negative_comment_vote(self):
        self.vote = False
        self.save()
