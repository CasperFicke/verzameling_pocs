# Generated by Django 3.2 on 2021-12-01 18:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0034_auto_20211201_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ontvanger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100, verbose_name='ontvanger')),
                ('beschrijving', models.CharField(blank=True, max_length=200, verbose_name='beschrijving')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True)),
                ('start_at', models.DateField(auto_now=True, help_text='Start date of the record', verbose_name='start at')),
                ('end_at', models.DateField(blank=True, editable=False, help_text='End date of the record', null=True, verbose_name='end at')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date of registration')),
            ],
            options={
                'verbose_name_plural': 'ontvangers',
                'ordering': ['naam'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100, verbose_name='teamnaam')),
            ],
            options={
                'verbose_name_plural': 'teams',
                'ordering': ['naam'],
            },
        ),
        migrations.AlterField(
            model_name='betrokkene',
            name='beschrijving',
            field=models.CharField(blank=True, max_length=200, verbose_name='beschrijving'),
        ),
        migrations.AlterField(
            model_name='grondslag',
            name='beschrijving',
            field=models.CharField(blank=True, max_length=200, verbose_name='beschrijving'),
        ),
        migrations.AlterField(
            model_name='persoonsgegevens',
            name='beschrijving',
            field=models.CharField(blank=True, max_length=200, verbose_name='beschrijving'),
        ),
        migrations.AlterField(
            model_name='verantwoordelijke',
            name='naam',
            field=models.CharField(max_length=100, verbose_name='verantwoordelijke'),
        ),
        migrations.AddField(
            model_name='verwerking',
            name='ontvangers',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Ontvanger'),
        ),
        migrations.AddField(
            model_name='verwerking',
            name='team',
            field=models.ManyToManyField(blank=True, to='verwerkingen.Team'),
        ),
    ]
