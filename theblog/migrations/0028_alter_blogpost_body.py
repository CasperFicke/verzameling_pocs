# Generated by Django 4.0 on 2021-12-29 16:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0027_alter_tag_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]