# Generated by Django 3.1.2 on 2020-11-12 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0055_auto_20201112_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 12, 20, 56, 16, 929625), verbose_name='زمان ارسال'),
        ),
    ]