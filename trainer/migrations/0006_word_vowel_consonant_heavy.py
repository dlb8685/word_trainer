# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0005_word_fragment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word_Vowel_Consonant_Heavy',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('vowel_heavy_flg', models.BooleanField()),
                ('vowel_count', models.SmallIntegerField()),
                ('consonant_heavy_flg', models.BooleanField()),
                ('consonant_count', models.SmallIntegerField()),
                ('word', models.ForeignKey(to='trainer.Word')),
            ],
        ),
    ]
