# Generated by Django 3.1.2 on 2020-11-13 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0026_auto_20201113_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 10, 25, 1, 727062), verbose_name='زمان ارسال'),
        ),
    ]