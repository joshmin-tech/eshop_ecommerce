# Generated by Django 3.2.3 on 2021-07-19 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secureadmin', '0004_usedoffer_is_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoffer',
            name='product',
        ),
        migrations.RemoveField(
            model_name='usedoffer',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='usedoffer',
            name='user',
        ),
        migrations.DeleteModel(
            name='CategoryOffer',
        ),
        migrations.DeleteModel(
            name='coupon',
        ),
        migrations.DeleteModel(
            name='ProductOffer',
        ),
        migrations.DeleteModel(
            name='UsedOffer',
        ),
    ]
