# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0002_auto_20160302_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word_stem',
            name='word_list',
        ),
    ]
