# Generated by Django 4.0 on 2021-12-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/profile/standard.jpg', null=True, upload_to='images/profile/'),
        ),
    ]