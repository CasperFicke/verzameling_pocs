# Generated by Django 3.2 on 2021-11-04 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domeinen', '0005_auto_20211104_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domein',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='subdomein',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
