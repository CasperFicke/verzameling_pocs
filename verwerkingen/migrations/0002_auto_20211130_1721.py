# Generated by Django 3.2 on 2021-11-30 16:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('verwerkingen', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persoonsgegevens',
            options={'verbose_name_plural': 'persoonsgegevens'},
        ),
        migrations.AlterModelOptions(
            name='verantwoordelijke',
            options={'verbose_name_plural': 'verantwoordelijken'},
        ),
        migrations.AlterField(
            model_name='betrokkene',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True),
        ),
        migrations.AlterField(
            model_name='grondslag',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True),
        ),
        migrations.AlterField(
            model_name='persoonsgegevens',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True),
        ),
        migrations.AlterField(
            model_name='verwerking',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier (UUID4)', unique=True),
        ),
    ]
