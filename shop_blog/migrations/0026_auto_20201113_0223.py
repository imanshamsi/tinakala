# Generated by Django 3.1.2 on 2020-11-12 22:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0025_auto_20201113_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 2, 23, 47, 30351), verbose_name='زمان ارسال'),
        ),
    ]