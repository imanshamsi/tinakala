# Generated by Django 3.1.2 on 2020-11-09 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_contact', '0017_auto_20201109_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userticket',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 21, 23, 46, 8004), verbose_name='زمان ایجاد تیکت'),
        ),
        migrations.AlterField(
            model_name='userticketanswer',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 21, 23, 46, 9001), verbose_name='زمان پاسخ تیکت'),
        ),
    ]