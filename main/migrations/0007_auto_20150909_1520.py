# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_mainpagesection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainpagesection',
            options={'verbose_name': "Section page d'acceuil", 'verbose_name_plural': "Sections page d'accueil", 'ordering': ('pk',)},
        ),
        migrations.AlterField(
            model_name='mainpagesection',
            name='content',
            field=models.TextField(verbose_name='Contenu'),
        ),
    ]
