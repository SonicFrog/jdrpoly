# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_auto_20150823_2142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='code',
            options={'verbose_name': 'Codes', 'ordering': ('pk',)},
        ),
        migrations.AlterField(
            model_name='code',
            name='content',
            field=models.CharField(max_length=30, verbose_name='Code', unique=True),
        ),
        migrations.AlterField(
            model_name='code',
            name='semesters',
            field=models.IntegerField(choices=[('Annuelle', 2), ('Semestrielle', 1)], verbose_name='Durée'),
        ),
    ]
