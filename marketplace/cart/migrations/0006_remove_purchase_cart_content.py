# Generated by Django 4.2.5 on 2023-10-06 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_purchase_devices_purchase_cart_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='cart_content',
        ),
    ]
