# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 10:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0007_auto_20160304_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('header', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('Reference', 'Reference'), ('Notice', 'Notice'), ('Reminder', 'Reminder'), ('TODO', 'TODO')], default='Notice', max_length=15)),
                ('favorites', models.BooleanField(default=False)),
                ('publish', models.BooleanField(default=False)),
                ('uu_id', models.CharField(default=uuid.uuid1, editable=False, max_length=100, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='note',
            name='author',
        ),
        migrations.RemoveField(
            model_name='note',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]
