# Generated by Django 5.0.6 on 2024-06-09 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_alter_restaurantinfo_image'),
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.table'),
        ),
        migrations.DeleteModel(
            name='Table',
        ),
    ]
