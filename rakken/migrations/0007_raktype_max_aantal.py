# Generated by Django 4.0 on 2022-08-31 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0006_raktype_rak'),
    ]

    operations = [
        migrations.AddField(
            model_name='raktype',
            name='max_aantal',
            field=models.PositiveIntegerField(null=True, verbose_name='Maximaal aantal keren te varen'),
        ),
    ]