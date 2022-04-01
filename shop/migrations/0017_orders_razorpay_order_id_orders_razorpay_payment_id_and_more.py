# Generated by Django 4.0.3 on 2022-03-24 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_orders_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='razorpay_order_id',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='orders',
            name='razorpay_payment_id',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='orders',
            name='razorpay_signature',
            field=models.CharField(default='', max_length=500),
        ),
    ]