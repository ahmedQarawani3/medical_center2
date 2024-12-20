# Generated by Django 5.1.3 on 2024-12-20 08:20

import patients.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_notification_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[patients.models.validate_phone_number]),
        ),
        migrations.AlterField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
