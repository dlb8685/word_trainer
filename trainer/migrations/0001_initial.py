# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('word', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Word_Prefix_Suffix_List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('prefix_list', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=1))),
                ('suffix_list', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=1))),
                ('word', models.ForeignKey(to='trainer.Word')),
            ],
        ),
        migrations.CreateModel(
            name='Word_Stem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('word_stem', models.TextField()),
                ('letter_combo_count', models.SmallIntegerField()),
                ('letter_combo_list', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=7))),
                ('letter_combo_likelihood', models.FloatField(default=0)),
                ('word_count', models.SmallIntegerField()),
                ('word_list', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.CharField(max_length=7))),
            ],
        ),
    ]
