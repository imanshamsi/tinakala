# Generated by Django 3.1.2 on 2020-11-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_contact', '0004_userticket_userticketanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userticketanswer',
            name='read',
            field=models.BooleanField(default=False, verbose_name='خوانده شده/نشده'),
        ),
    ]