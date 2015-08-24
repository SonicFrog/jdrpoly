# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20150722_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('content', models.TextField(max_length=30)),
                ('semesters', models.IntegerField(choices=[('Annuelle', 2), ('Semestrielle', 1)])),
            ],
        ),
    ]
