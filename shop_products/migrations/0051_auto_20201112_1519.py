# Generated by Django 3.1.2 on 2020-11-12 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0050_auto_20201111_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 12, 15, 19, 21, 684327), verbose_name='زمان ارسال'),
        ),
    ]