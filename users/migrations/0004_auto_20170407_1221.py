# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-07 09:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170405_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email_confirmed',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
    ]
