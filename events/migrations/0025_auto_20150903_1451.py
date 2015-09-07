# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20150903_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventparticipation',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventparticipation',
            name='user',
        ),
        migrations.AlterField(
            model_name='edition',
            name='gallery',
            field=models.ForeignKey(blank=True, verbose_name='Gallerie photo', to='pictures.Gallery'),
        ),
        migrations.DeleteModel(
            name='EventParticipation',
        ),
    ]
