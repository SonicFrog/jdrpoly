# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_eventpicture_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpicture',
            name='date',
            field=models.DateTimeField(verbose_name='Date', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='eventpicture',
            name='description',
            field=models.CharField(verbose_name='Description', max_length=200, default='Photo'),
        ),
        migrations.AlterField(
            model_name='eventpicture',
            name='filename',
            field=models.ImageField(upload_to='', verbose_name='Image', default='Nouvelle photo'),
        ),
    ]
