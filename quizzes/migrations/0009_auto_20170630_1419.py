# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 14:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0008_auto_20170629_1513'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useranswer',
            options={'ordering': ['quiz_attempt_id']},
        ),
    ]
