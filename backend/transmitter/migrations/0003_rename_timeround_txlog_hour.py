# Generated by Django 4.0.6 on 2022-12-13 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transmitter', '0002_txlog_added_txlog_modified_txlog_timeround'),
    ]

    operations = [
        migrations.RenameField(
            model_name='txlog',
            old_name='timeround',
            new_name='hour',
        ),
    ]
