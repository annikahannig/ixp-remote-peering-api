# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-05 13:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remote_peering', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='ixps',
        ),
        migrations.RemoveField(
            model_name='member',
            name='ixps',
        ),
    ]
