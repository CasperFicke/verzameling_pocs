# Generated by Django 4.0 on 2022-01-11 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('energie', '0012_remove_meter_medium'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meter',
            old_name='med',
            new_name='medium',
        ),
    ]
