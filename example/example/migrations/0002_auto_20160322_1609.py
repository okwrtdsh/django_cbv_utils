# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mymodel',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='mymodel',
            name='name2',
            field=models.CharField(verbose_name='name2', default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mymodel',
            name='status',
            field=models.IntegerField(verbose_name='status', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
    ]
