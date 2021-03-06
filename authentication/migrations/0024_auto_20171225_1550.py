# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-25 12:50
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0023_connection_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=imagekit.models.fields.ProcessedImageField(default='profiles/default.jpg', upload_to='profiles'),
        ),
    ]
