# Generated by Django 3.1.2 on 2020-10-25 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0017_auto_20201025_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 22, 58, 21, 485877), verbose_name='زمان ارسال'),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='title',
            field=models.CharField(max_length=120, verbose_name='عنوان نظر'),
        ),
    ]