# Generated by Django 3.1.2 on 2020-10-24 14:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop_products', '0006_auto_20201024_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(default=uuid.uuid4, max_length=12, verbose_name='کد محصول'),
        ),
    ]