# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webclient', '0003_auto_20150831_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='created_by',
        ),
    ]
