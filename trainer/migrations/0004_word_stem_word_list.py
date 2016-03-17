# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0003_remove_word_stem_word_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='word_stem',
            name='word_list',
            field=django.contrib.postgres.fields.ArrayField(size=None, base_field=models.IntegerField(), null=True),
        ),
    ]
