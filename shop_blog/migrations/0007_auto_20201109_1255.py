# Generated by Django 3.1.2 on 2020-11-09 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0006_auto_20201106_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 12, 55, 45, 774987), verbose_name='زمان ارسال'),
        ),
    ]