# Generated by Django 3.2 on 2021-11-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domeinen', '0011_auto_20211105_1331'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='certificaat',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='certificaat',
            name='url',
        ),
        migrations.AddField(
            model_name='certificaat',
            name='url',
            field=models.ManyToManyField(blank=True, to='domeinen.Domein'),
        ),
    ]
