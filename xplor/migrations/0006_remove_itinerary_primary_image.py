# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 16:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xplor', '0005_itinerary_primary_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itinerary',
            name='primary_image',
        ),
    ]
