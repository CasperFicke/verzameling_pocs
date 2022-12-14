# Generated by Django 4.0 on 2021-12-13 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_alter_land_aant_inwoners'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plaats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100, unique=True)),
                ('aant_inwoners', models.PositiveIntegerField(null=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'plaatsen',
            },
        ),
    ]
