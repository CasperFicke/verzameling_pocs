# Generated by Django 4.0 on 2021-12-27 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0003_measurement_bearing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='distance',
        ),
        migrations.AddField(
            model_name='measurement',
            name='dist_km',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='dist_nm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
