# Generated by Django 3.1.1 on 2021-03-30 12:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20210319_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique identifier (UUID4)', unique=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(help_text='Name of the venue', max_length=255, verbose_name='Venue Name'),
        ),
    ]
