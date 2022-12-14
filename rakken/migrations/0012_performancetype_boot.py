# Generated by Django 4.0 on 2022-09-09 13:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0011_rak_lengte'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100, verbose_name='Naam van dit performancetype')),
                ('beschrijving', models.TextField(blank=True, verbose_name='Beschrijving')),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='Unique identifier (UUID4)', unique=True)),
                ('start_at', models.DateField(auto_now=True, help_text='Start date of the performancetype record', verbose_name='start at')),
                ('end_at', models.DateField(blank=True, editable=False, help_text='End date of the performancetype record', null=True, verbose_name='end at')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date when the performancetype was registered in the system')),
            ],
            options={
                'verbose_name_plural': 'performance types',
            },
        ),
        migrations.CreateModel(
            name='Boot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(help_text='Naam van de boot', max_length=255, verbose_name='Bootnaam')),
                ('type', models.CharField(help_text='Type boot', max_length=255, verbose_name='Boot type')),
                ('toelichting', models.TextField(blank=True, help_text='Toelichting bij deze boot', verbose_name='Boot toelichting')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True)),
                ('start_at', models.DateField(auto_now=True, help_text='Start date of the boot record', verbose_name='start at')),
                ('end_at', models.DateField(blank=True, help_text='End date of the boot record', null=True, verbose_name='end at')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date when the boot was registered in the system')),
                ('performance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boten', to='rakken.performancetype')),
            ],
            options={
                'verbose_name_plural': 'boten',
            },
        ),
    ]
