# Generated by Django 4.0 on 2022-09-28 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0027_remove_rak_distance_alter_rak_lengte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rak',
            name='bearing12',
        ),
        migrations.RemoveField(
            model_name='rak',
            name='bearing21',
        ),
    ]
