# Generated by Django 3.1.2 on 2020-11-09 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0038_auto_20201109_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 20, 39, 14, 127960), verbose_name='زمان ارسال'),
        ),
    ]