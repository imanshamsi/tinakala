import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from shop_accounts.models import UserAddress
from shop_products.models import Product


class Order(models.Model):
    PAID_CHOICES = (
        (True, 'پرداخت شده'),
        (False, 'پرداخت نشده'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='مربوط به کاربر')
    address = models.ForeignKey(UserAddress, on_delete=models.PROTECT, verbose_name='ارسال به آدرس')
    order_date = models.DateTimeField(auto_now_add=True)
    order_code = models.CharField(max_length=12, null=True, blank=True, verbose_name='کد سفارش')
    is_paid = models.BooleanField(default=False, choices=PAID_CHOICES, verbose_name='پرداخت شده/نشده')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'مدیریت سبد خرید'

    def __str__(self):
        return f'{self.customer.get_full_name()}-{self.order_date}'

    def get_total_price(self):
        items = self.orderitem_set.all()
        amount = 0
        for item in items:
            amount += item.product_cost
        return amount

    def get_nice_total_price(self):
        return f'{self.get_total_price():,}'


@receiver(pre_save, sender=Order)
def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_code:
        instance.order_code = f'tko-{str(uuid.uuid4())[0:8]}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='مربوط به سبد خرید')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name='محصول')
    product_price = models.PositiveBigIntegerField(verbose_name='قیمت محصول')
    product_count = models.IntegerField(verbose_name='تعداد محصول')
    product_cost = models.IntegerField(null=True, blank=True, verbose_name='هزینه کل محصول')

    class Meta:
        verbose_name = 'محصول در سبد'
        verbose_name_plural = 'مدیریت محصولات در سبد'

    def __str__(self):
        return f'{self.order.customer.get_full_name()}-{self.order.id}-{self.product.title}'

    def get_nice_price(self):
        return f'{self.product_price:,}'

    def get_nice_total_price(self):
        return f'{self.product_count * self.product_price:,}'


@receiver(pre_save, sender=OrderItem)
def order_item_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.product_cost = instance.product_count * instance.product_price


class Invoice(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, verbose_name='مربوط به سبد')
    invoice_date = models.DateTimeField(auto_now_add=True)
    authority = models.CharField(max_length=200, verbose_name='کد اعتبار')

    class Meta:
        verbose_name = 'صورتحساب'
        verbose_name_plural = 'مدیریت صورتحساب ها'

    def __str__(self):
        return f'{self.order.customer.get_full_name()}-{self.id}'


class Transaction(models.Model):
    STATUS_CHOICES = (
        (1, 'در انتظار بررسی'),
        (0, 'سفارش لغو شده'),
        (2, 'سفارش کامل شده'),
    )
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL, verbose_name='مربوط به صورت حساب')
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مقدار کل')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='وضعیت سفارش')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'مدیریت تراکنش ها'

    def __str__(self):
        return f'{self.invoice.order.customer.get_full_name()}-{self.id}'
