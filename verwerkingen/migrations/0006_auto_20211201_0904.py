# Generated by Django 3.2 on 2021-12-01 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0005_auto_20211201_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verwerking',
            name='grondslag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verwerkingen', to='verwerkingen.grondslag'),
        ),
        migrations.RemoveField(
            model_name='verwerking',
            name='verantwoordelijke',
        ),
        migrations.AddField(
            model_name='verwerking',
            name='verantwoordelijke',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verwerkingen', to='verwerkingen.verantwoordelijke'),
        ),
    ]
