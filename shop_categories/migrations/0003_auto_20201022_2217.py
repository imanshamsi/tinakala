# Generated by Django 3.1.2 on 2020-10-22 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_categories', '0002_auto_20201022_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategoryparent',
            name='main_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_categories.category', verbose_name='دسته والد'),
        ),
    ]