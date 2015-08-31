# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'ordering': ('-date',), 'verbose_name_plural': 'Galleries', 'verbose_name': 'Gallerie'},
        ),
        migrations.AlterField(
            model_name='picture',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Mise en ligne'),
        ),
    ]
