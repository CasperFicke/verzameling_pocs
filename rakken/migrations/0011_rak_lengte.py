# Generated by Django 4.0 on 2022-09-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0010_evenement_rak_evenement'),
    ]

    operations = [
        migrations.AddField(
            model_name='rak',
            name='lengte',
            field=models.FloatField(blank=True, null=True, verbose_name='Rak-lengte'),
        ),
    ]
