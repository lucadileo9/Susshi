# Generated by Django 5.0.6 on 2024-06-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_delete_contactinfo_delete_restaurantinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('da confermare', 'Da confermare'), ('confermato', 'Confermato')], default='da confermare', max_length=20),
        ),
    ]
