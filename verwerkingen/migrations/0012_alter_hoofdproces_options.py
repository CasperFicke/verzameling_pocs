# Generated by Django 3.2 on 2021-12-01 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0011_hoofdproces'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hoofdproces',
            options={'ordering': ['naam'], 'verbose_name_plural': 'hoofdprocessen'},
        ),
    ]
