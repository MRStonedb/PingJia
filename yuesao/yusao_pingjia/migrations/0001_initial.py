# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pingjia_info',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('uname', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=1024)),
                ('time', models.CharField(max_length=100)),
                ('score', models.CharField(max_length=100)),
            ],
        ),
    ]
