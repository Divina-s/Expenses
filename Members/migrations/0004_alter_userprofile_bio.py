# Generated by Django 4.2.2 on 2023-06-19 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0003_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(null=True),
        ),
    ]