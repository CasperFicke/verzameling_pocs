# Generated by Django 4.0 on 2022-01-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0012_hook_actie'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actie',
            options={'verbose_name_plural': 'acties'},
        ),
        migrations.RemoveField(
            model_name='actie',
            name='hook',
        ),
        migrations.AddField(
            model_name='hook',
            name='actie',
            field=models.ManyToManyField(blank=True, to='maps.Actie'),
        ),
    ]
