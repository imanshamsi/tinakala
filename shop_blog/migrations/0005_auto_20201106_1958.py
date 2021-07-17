# Generated by Django 3.1.2 on 2020-11-06 16:28

import datetime
from django.db import migrations, models
import django_resized.forms
import tinakala.utils.upload_file_manager


class Migration(migrations.Migration):

    dependencies = [
        ('shop_blog', '0004_auto_20201106_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=150, size=[360, 225], upload_to=tinakala.utils.upload_file_manager.upload_blog_avatar, verbose_name='آواتار مقاله'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 19, 58, 36, 934047), verbose_name='زمان ارسال'),
        ),
    ]