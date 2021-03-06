# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 21:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0002_auto_20150831_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'ordering': ('-date',), 'verbose_name': 'Galerie', 'verbose_name_plural': 'Galeries'},
        ),
        migrations.AlterField(
            model_name='picture',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='pictures.Gallery', verbose_name='Galerie'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(default=None, upload_to='svz/pictures/%Y-%m-%d', verbose_name='Image'),
        ),
    ]
