# Generated by Django 3.2 on 2021-12-01 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0020_remove_verwerking_gemeente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verwerking',
            name='persoonsgegevens',
        ),
    ]