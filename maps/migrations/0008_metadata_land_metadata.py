# Generated by Django 4.0 on 2021-12-24 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0007_unemploymentrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=100, unique=True)),
                ('beschrijving', models.TextField(blank=True, max_length=400, null=True)),
                ('referentie', models.URLField(blank=True, max_length=100, null=True)),
                ('beheerder', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'metadata',
            },
        ),
        migrations.AddField(
            model_name='land',
            name='metadata',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='maps.metadata'),
        ),
    ]