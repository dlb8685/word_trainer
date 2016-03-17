# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0004_word_stem_word_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word_Fragment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('word_fragment', models.TextField()),
                ('word_count', models.SmallIntegerField()),
                ('word_list', django.contrib.postgres.fields.ArrayField(null=True, base_field=models.IntegerField(), size=None)),
            ],
        ),
    ]
