# Generated by Django 3.1.2 on 2020-11-13 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0032_auto_20201113_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 19, 54, 9, 362532), verbose_name='زمان ارسال'),
        ),
    ]