# Generated by Django 3.2 on 2021-11-05 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domeinen', '0012_auto_20211105_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificaat',
            old_name='url',
            new_name='domeinen',
        ),
        migrations.AddField(
            model_name='certificaat',
            name='subdomeinen',
            field=models.ManyToManyField(blank=True, to='domeinen.Subdomein'),
        ),
    ]
