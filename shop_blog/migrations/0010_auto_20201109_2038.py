# Generated by Django 3.1.2 on 2020-11-09 17:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0009_auto_20201109_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 20, 38, 56, 911396), verbose_name='زمان ارسال'),
        ),
    ]