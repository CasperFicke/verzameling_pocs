# Generated by Django 3.2 on 2021-12-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0024_persoonsgegevens'),
    ]

    operations = [
        migrations.AddField(
            model_name='verwerking',
            name='persoonsgegevens',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Persoonsgegevens'),
        ),
    ]
