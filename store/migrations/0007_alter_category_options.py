# Generated by Django 4.0 on 2021-12-21 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_category_alter_orderitem_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
