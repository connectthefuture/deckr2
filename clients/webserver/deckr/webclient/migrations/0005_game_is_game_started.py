# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webclient', '0004_remove_game_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_game_started',
            field=models.BooleanField(default=False),
        ),
    ]
