# Generated by Django 4.0 on 2022-08-10 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0036_verordening_verwerking_reden_grondslag_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persoonsgegeven',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='type persoonsgegeven')),
                ('beschrijving', models.CharField(blank=True, max_length=200, verbose_name='beschrijving')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True)),
                ('start_at', models.DateField(auto_now=True, help_text='Start date of the record', verbose_name='start at')),
                ('end_at', models.DateField(blank=True, editable=False, help_text='End date of the record', null=True, verbose_name='end at')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date of registration')),
            ],
            options={
                'verbose_name_plural': 'persoonsgegevens',
                'ordering': ['type'],
            },
        ),
        migrations.DeleteModel(
            name='Persoonsgegevens',
        ),
        migrations.AlterField(
            model_name='verwerking',
            name='persoonsgegevens',
            field=models.ManyToManyField(blank=True, related_name='verwerkingen', to='verwerkingen.Persoonsgegeven'),
        ),
    ]
