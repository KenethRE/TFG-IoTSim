# Generated by Django 5.0.2 on 2024-03-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starthere', '0005_devices'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='Value',
            field=models.CharField(default='0', max_length=50),
        ),
    ]
