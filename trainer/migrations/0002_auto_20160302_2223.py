# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word_prefix_suffix_list',
            name='prefix_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='word_prefix_suffix_list',
            name='suffix_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), null=True, size=None),
        ),
    ]
