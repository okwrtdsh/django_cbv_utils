# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='created')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('birthday', models.DateField(verbose_name='birthday')),
                ('number', models.IntegerField(verbose_name='number')),
                ('status', models.IntegerField(verbose_name='status', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
            ],
        ),
    ]
