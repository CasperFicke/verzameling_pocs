# Generated by Django 4.0 on 2022-09-28 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0026_alter_baan_windkracht_alter_baan_windrichting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rak',
            name='distance',
        ),
        migrations.AlterField(
            model_name='rak',
            name='lengte',
            field=models.FloatField(blank=True, null=True, verbose_name='Raklengte volgens organisatie'),
        ),
    ]
