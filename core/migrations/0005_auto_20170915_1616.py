# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-15 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_auto_20170717_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='user',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mentorshiparea',
            name='user',
        ),
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Experience',
        ),
        migrations.DeleteModel(
            name='MentorshipArea',
        ),
    ]
