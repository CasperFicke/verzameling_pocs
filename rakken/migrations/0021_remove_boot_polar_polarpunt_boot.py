# Generated by Django 4.0 on 2022-09-24 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rakken', '0020_polarpunttype_polarpunt_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boot',
            name='polar',
        ),
        migrations.AddField(
            model_name='polarpunt',
            name='boot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polarpunten', to='rakken.boot'),
        ),
    ]
