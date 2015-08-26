# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, default='Nouvelle galerie', verbose_name='Nom')),
                ('description', models.TextField(default=None, verbose_name='Description')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Création')),
            ],
            options={
                'verbose_name': 'Galleries',
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', default=None, verbose_name='Image')),
                ('comment', models.CharField(max_length=100, default=None, verbose_name='Commentaire')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('gallery', models.ForeignKey(related_name='pictures', to='pictures.Gallery', verbose_name='Gallerie')),
                ('owner', models.ForeignKey(related_name='pictures', to=settings.AUTH_USER_MODEL, verbose_name='Uploadeur')),
            ],
            options={
                'verbose_name': 'Photo',
                'ordering': ('-date',),
                'verbose_name_plural': 'Photos',
            },
        ),
    ]
