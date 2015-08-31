# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webclient', '0002_remove_game_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='id',
        ),
        migrations.AlterField(
            model_name='game',
            name='game_id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
