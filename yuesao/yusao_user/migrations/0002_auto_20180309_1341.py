# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yusao_user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='uemail',
            new_name='uphone',
        ),
    ]
