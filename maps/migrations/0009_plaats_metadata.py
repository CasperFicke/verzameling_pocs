# Generated by Django 4.0 on 2021-12-24 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0008_metadata_land_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='plaats',
            name='metadata',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='maps.metadata'),
        ),
    ]
