# Generated by Django 3.2 on 2021-12-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0002_alter_land_naam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='naam',
            field=models.CharField(max_length=100),
        ),
    ]
