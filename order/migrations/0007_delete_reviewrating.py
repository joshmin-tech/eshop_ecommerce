# Generated by Django 3.2.3 on 2021-07-20 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_coupon_offer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReviewRating',
        ),
    ]
