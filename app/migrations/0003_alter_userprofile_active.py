# Generated by Django 4.0.5 on 2022-09-24 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userprofile_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='active',
            field=models.CharField(choices=[('ONLINE', 'ONLINE'), ('OFFLINE', 'OFFLINE')], max_length=100, null=True),
        ),
    ]
