# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-02 17:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_text', models.TextField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2016, 3, 2, 20, 45, 14, 377929))),
            ],
        ),
    ]