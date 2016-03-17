# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0006_word_vowel_consonant_heavy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word_OLaughlin_Score',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('olaughlin_score', models.IntegerField()),
                ('word', models.ForeignKey(to='trainer.Word')),
            ],
        ),
    ]
