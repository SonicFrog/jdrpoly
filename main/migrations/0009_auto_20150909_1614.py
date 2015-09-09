# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_mainpagesection_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainpagesection',
            options={'verbose_name': "Section page d'acceuil", 'ordering': ('order', '-pk'), 'verbose_name_plural': "Sections page d'accueil"},
        ),
        migrations.AlterField(
            model_name='mainpagesection',
            name='order',
            field=models.IntegerField(verbose_name='Position'),
        ),
    ]
