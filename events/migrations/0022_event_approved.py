# Generated by Django 4.0 on 2022-01-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
