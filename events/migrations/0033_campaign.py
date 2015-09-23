# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0032_event_member_only'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('min_player', models.IntegerField(verbose_name='Minimum de joueurs')),
                ('max_player', models.IntegerField(verbose_name='Maximum de joueurs')),
                ('open_for_registration', models.BooleanField(verbose_name='Accepte les nouveaux joueurs')),
                ('description', models.TextField(verbose_name='Description')),
                ('name', models.TextField(verbose_name='Nom', max_length=200)),
                ('edition', models.ForeignKey(related_name='campaigns', verbose_name='Début', to='events.Edition')),
                ('participants', models.ManyToManyField(related_name='campaigns', verbose_name='Participants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Campagne',
                'verbose_name_plural': 'Campagnes',
                'ordering': ('-edition',),
            },
        ),
    ]
