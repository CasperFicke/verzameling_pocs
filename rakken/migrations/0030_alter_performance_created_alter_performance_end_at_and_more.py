# Generated by Django 4.0 on 2022-10-03 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0029_rakscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='end_at',
            field=models.DateField(blank=True, help_text='End date of the record', null=True, verbose_name='end at'),
        ),
        migrations.AlterField(
            model_name='performance',
            name='start_at',
            field=models.DateField(auto_now=True, help_text='Start date of the record', verbose_name='start at'),
        ),
        migrations.AlterField(
            model_name='rak',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system'),
        ),
        migrations.AlterField(
            model_name='rak',
            name='end_at',
            field=models.DateField(blank=True, help_text='End date of the record', null=True, verbose_name='end at'),
        ),
        migrations.AlterField(
            model_name='rak',
            name='start_at',
            field=models.DateField(auto_now=True, help_text='Start date of the record', verbose_name='start at'),
        ),
        migrations.AlterField(
            model_name='raktype',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system'),
        ),
        migrations.AlterField(
            model_name='raktype',
            name='end_at',
            field=models.DateField(blank=True, editable=False, help_text='End date of the record', null=True, verbose_name='end at'),
        ),
        migrations.AlterField(
            model_name='raktype',
            name='start_at',
            field=models.DateField(auto_now=True, help_text='Start date of the record', verbose_name='start at'),
        ),
    ]
