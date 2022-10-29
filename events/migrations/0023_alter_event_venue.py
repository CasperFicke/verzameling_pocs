# Generated by Django 4.0 on 2022-02-10 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_event_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, help_text='Venue this event takes place', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.venue'),
        ),
    ]