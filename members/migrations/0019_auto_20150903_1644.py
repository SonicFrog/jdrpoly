# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_member_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='semesters',
            field=models.IntegerField(choices=[(2, 'Annuelle'), (1, 'Semestrielle')], verbose_name='Durée'),
        ),
    ]
