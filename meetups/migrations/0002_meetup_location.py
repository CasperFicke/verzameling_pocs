# Generated by Django 4.0 on 2021-12-13 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetup',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
