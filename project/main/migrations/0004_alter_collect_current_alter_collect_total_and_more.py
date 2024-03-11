# Generated by Django 4.2.11 on 2024-03-11 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_alter_collect_donaters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='current',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Собрано средств'),
        ),
        migrations.AlterField(
            model_name='collect',
            name='total',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Сумма для сбора'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='main.collect', verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Донатер'),
        ),
    ]