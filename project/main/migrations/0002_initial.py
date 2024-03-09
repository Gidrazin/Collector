# Generated by Django 4.2.11 on 2024-03-09 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donater', to=settings.AUTH_USER_MODEL, verbose_name='Донатер'),
        ),
        migrations.AddField(
            model_name='collect',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collects', to=settings.AUTH_USER_MODEL, verbose_name='Инициатор сбора'),
        ),
        migrations.AddField(
            model_name='collect',
            name='donaters',
            field=models.ManyToManyField(to='main.payment'),
        ),
        migrations.AddConstraint(
            model_name='payment',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_event_donation'),
        ),
    ]
