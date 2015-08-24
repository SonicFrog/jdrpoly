# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20150819_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'Profile'},
        ),
        migrations.AlterField(
            model_name='code',
            name='content',
            field=models.TextField(unique=True, max_length=30, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='code',
            name='semesters',
            field=models.IntegerField(choices=[('Annuelle', 2), ('Semestrielle', 1)], verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(upload_to='', default=None, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_member',
            field=models.BooleanField(default=False, verbose_name='Membre actif ?'),
        ),
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.CharField(max_length=200, default=None, verbose_name='Localisation'),
        ),
        migrations.AlterField(
            model_name='member',
            name='until',
            field=models.DateField(default=django.utils.timezone.now, verbose_name="Membre jusqu'à"),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
    ]
