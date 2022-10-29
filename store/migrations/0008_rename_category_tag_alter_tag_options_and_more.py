# Generated by Django 4.0 on 2021-12-22 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_category_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Tag',
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': 'tags'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='store.Tag'),
        ),
    ]