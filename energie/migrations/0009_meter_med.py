# Generated by Django 4.0 on 2022-01-11 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('energie', '0008_medium'),
    ]

    operations = [
        migrations.AddField(
            model_name='meter',
            name='med',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='energie.medium'),
        ),
    ]