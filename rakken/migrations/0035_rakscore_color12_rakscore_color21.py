# Generated by Django 4.0 on 2022-10-05 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0034_rakscore_score12_rakscore_score21_rakscore_twa12_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rakscore',
            name='color12',
            field=models.TextField(blank=True, null=True, verbose_name='kleurscore van waypoint1 naar waypoint2'),
        ),
        migrations.AddField(
            model_name='rakscore',
            name='color21',
            field=models.TextField(blank=True, null=True, verbose_name='kleurscore van waypoint2 naar waypoint1'),
        ),
    ]
