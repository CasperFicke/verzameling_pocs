# Generated by Django 3.2 on 2021-12-01 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0033_verwerking_hoofdproces'),
    ]

    operations = [
        migrations.AddField(
            model_name='verwerking',
            name='betrokkenen',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Betrokkene'),
        ),
        migrations.AddField(
            model_name='verwerking',
            name='persoonsgegevens',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Persoonsgegevens'),
        ),
        migrations.AddField(
            model_name='verwerking',
            name='verantwoordelijke',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verwerkingen', to='verwerkingen.verantwoordelijke'),
        ),
    ]
