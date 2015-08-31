# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150823_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Auteur'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(max_length=10000, verbose_name='Contenu'),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=200, default='Nouvelle news', verbose_name='Titre'),
        ),
    ]
