# Generated by Django 4.0.5 on 2022-09-24 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_friendlist_lastseen_chatroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='msg',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='status',
            field=models.BooleanField(),
        ),
    ]