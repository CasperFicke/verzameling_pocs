# Generated by Django 3.1.1 on 2021-03-30 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20210330_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='uuid',
        ),
    ]
