# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0033_campaign'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaign',
            options={'verbose_name': 'Campagne', 'verbose_name_plural': 'Campagnes', 'ordering': ('-start',)},
        ),
        migrations.RenameField(
            model_name='campaign',
            old_name='max_player',
            new_name='max_players',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='edition',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='min_player',
        ),
        migrations.AddField(
            model_name='campaign',
            name='duration',
            field=models.DurationField(verbose_name='Durée', default=datetime.timedelta(1)),
        ),
        migrations.AddField(
            model_name='campaign',
            name='owner',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='Créateur', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='start',
            field=models.DateField(verbose_name='Début', default=django.utils.timezone.now),
        ),
    ]
