# Generated by Django 4.0 on 2021-12-13 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_alter_land_naam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='aant_inwoners',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
