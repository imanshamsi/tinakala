# Generated by Django 3.1.2 on 2020-11-09 17:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0037_auto_20201109_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 20, 38, 56, 901422), verbose_name='زمان ارسال'),
        ),
    ]