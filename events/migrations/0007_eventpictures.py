# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150722_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('filename', models.TextField(default='Nouvelle photo')),
                ('event', models.ForeignKey(to='events.Event')),
            ],
        ),
    ]
