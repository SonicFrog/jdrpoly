# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150831_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPageSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('content', models.CharField(max_length=2000, verbose_name='Contenu')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': "Sections page d'acceuil",
            },
        ),
    ]
