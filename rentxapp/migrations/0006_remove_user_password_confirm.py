# Generated by Django 2.2.4 on 2022-10-12 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentxapp', '0005_auto_20221012_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password_confirm',
        ),
    ]
