# Generated by Django 4.2.11 on 2024-03-11 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_collect_donaters_cnt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collect',
            name='donaters',
        ),
    ]
