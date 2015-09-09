# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150909_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComityMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('first_name', models.CharField(verbose_name='Prénom', max_length=100)),
                ('last_name', models.CharField(verbose_name='Nom', max_length=100)),
                ('post', models.CharField(verbose_name='Poste', max_length=100)),
                ('description', models.TextField(verbose_name='Description du poste')),
                ('email', models.EmailField(verbose_name='Addresse de contact', max_length=254)),
            ],
            options={
                'verbose_name': 'Membre du comité',
                'verbose_name_plural': 'Membres du comité',
                'ordering': ('pk',),
            },
        ),
    ]
