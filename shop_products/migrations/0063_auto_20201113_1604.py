# Generated by Django 3.1.2 on 2020-11-13 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0062_auto_20201113_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 16, 4, 25, 988558), verbose_name='زمان ارسال'),
        ),
    ]