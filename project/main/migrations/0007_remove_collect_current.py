# Generated by Django 4.2.11 on 2024-03-11 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_collect_donaters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collect',
            name='current',
        ),
    ]
