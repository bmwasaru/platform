# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-09-11 12:39
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_auto_20170911_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mentorship_areas',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('academic_assistance', 'Academic Assistance'), ('entrepreneurship', 'Entrepreneurship (Having difficulties being your own boss?)'), ('career_counceling', 'Career Counceling'), ('career_readiness', 'Career readiness (Interviews or Job hunting)'), ('grief_loss', 'Coping with grief and loss'), ('addictions', 'Coping with addictions'), ('abuse', 'Trauma and Abuse'), ('no_preference', 'Prefere not to answer')], default='', max_length=113),
        ),
    ]