# Generated by Django 3.1.2 on 2020-11-06 17:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0031_auto_20201105_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 21, 10, 10, 45795), verbose_name='زمان ارسال'),
        ),
    ]