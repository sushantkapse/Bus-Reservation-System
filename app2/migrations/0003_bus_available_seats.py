# Generated by Django 5.0 on 2024-07-03 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0002_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='available_seats',
            field=models.IntegerField(default=40),
        ),
    ]
