# Generated by Django 3.2 on 2021-12-01 14:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0029_delete_verwerking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verwerking',
            fields=[
                ('naam', models.CharField(max_length=200, verbose_name='verwerkingsactiviteit')),
                ('doel', models.CharField(max_length=250, verbose_name='reden van verwerking')),
                ('bewaartermijn', models.CharField(max_length=200, verbose_name='bewaartermijn')),
                ('buitenEUgedeeld', models.BooleanField(default=False, verbose_name='buiten de EU gedeeld')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', primary_key=True, serialize=False, unique=True)),
                ('start_at', models.DateField(auto_now=True, help_text='Start date of the record', verbose_name='start at')),
                ('end_at', models.DateField(blank=True, editable=False, help_text='End date of the record', null=True, verbose_name='end at')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date of registration')),
            ],
            options={
                'verbose_name_plural': 'verwerkingen',
                'ordering': ['naam'],
            },
        ),
    ]
