# Generated by Django 4.0.3 on 2022-03-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_rename_catagery_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(max_length=10000),
        ),
    ]
