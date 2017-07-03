# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 15:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizzes', '0007_auto_20170629_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='quiz_attempt_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='useranswer',
            unique_together=set([('user_answer', 'user', 'quiz_attempt_id')]),
        ),
    ]
