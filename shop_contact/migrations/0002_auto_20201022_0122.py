# Generated by Django 3.1.2 on 2020-10-21 21:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'پیام', 'verbose_name_plural': 'مدیریت پیام ها'},
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='answered',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='answered_at',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='متن پیام'),
        ),
    ]