# Generated by Django 5.0.6 on 2024-06-09 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_alter_order_table_delete_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContactInfo',
        ),
        migrations.DeleteModel(
            name='RestaurantInfo',
        ),
    ]
