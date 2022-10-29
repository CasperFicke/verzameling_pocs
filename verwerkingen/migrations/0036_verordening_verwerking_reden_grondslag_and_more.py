# Generated by Django 4.0 on 2022-08-10 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0035_auto_20211201_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verordening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100, verbose_name='verordening-naam')),
                ('beschrijving', models.CharField(blank=True, max_length=200, verbose_name='beschrijving')),
            ],
            options={
                'verbose_name_plural': 'verordeningen',
                'ordering': ['naam'],
            },
        ),
        migrations.AddField(
            model_name='verwerking',
            name='reden_grondslag',
            field=models.TextField(blank=True, max_length=250, verbose_name='reden van grondslag'),
        ),
        migrations.AlterField(
            model_name='verwerking',
            name='doel',
            field=models.TextField(max_length=250, verbose_name='doel van verwerking'),
        ),
        migrations.AlterField(
            model_name='verwerking',
            name='gemeente',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Gemeente'),
        ),
        migrations.AddField(
            model_name='verwerking',
            name='verordening',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Verordening'),
        ),
    ]