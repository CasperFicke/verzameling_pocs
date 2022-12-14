# Generated by Django 3.2 on 2021-06-01 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0016_auto_20210416_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(blank=True, help_text='Manager of the event', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='venue',
            name='start_at',
            field=models.DateField(auto_now=True, help_text='Start date of the venue record', verbose_name='start at'),
        ),
    ]
