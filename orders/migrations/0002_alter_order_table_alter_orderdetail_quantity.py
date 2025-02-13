# Generated by Django 5.0.6 on 2024-06-10 09:01

import django.db.models.deletion
import orders.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('tables', '0002_remove_table_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tables.table'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.PositiveIntegerField(default=1, validators=[orders.models.validate_positive_nonzero]),
        ),
    ]
