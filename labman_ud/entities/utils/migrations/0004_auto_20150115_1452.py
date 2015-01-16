# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_auto_20150115_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='rgb_color',
            field=models.CharField(max_length=6, null=True, verbose_name='RGB color (#)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='award',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='award',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='awardseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='awardseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cityseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cityseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contributionseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contributionseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contributiontype',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contributiontype',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='country',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='country',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='countryseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='countryseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileitem',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileitem',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileitemrelatedtocontribution',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileitemrelatedtocontribution',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileitemrelatedtotalkorcourse',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fileitemrelatedtotalkorcourse',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geographicalscope',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geographicalscope',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geographicalscopeseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='geographicalscopeseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='languageseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='languageseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='license',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='license',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='licenseseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='licenseseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='network',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='network',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='networkseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='networkseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personrelatedtoaward',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personrelatedtoaward',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personrelatedtocontribution',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personrelatedtocontribution',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personrelatedtotalkorcourse',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personrelatedtotalkorcourse',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phdprogram',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phdprogram',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phdprogramseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phdprogramseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectrelatedtoaward',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectrelatedtoaward',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectrelatedtocontribution',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectrelatedtocontribution',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectrelatedtotalkorcourse',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectrelatedtotalkorcourse',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrelatedtoaward',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrelatedtoaward',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrelatedtocontribution',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationrelatedtocontribution',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='role',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='role',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagrelatedtocontribution',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagrelatedtocontribution',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagrelatedtotalkorcourse',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagrelatedtotalkorcourse',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkorcourse',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkorcourse',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkorcourseseealso',
            name='log_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5567), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkorcourseseealso',
            name='log_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 15, 14, 52, 47, 5627), auto_now=True),
            preserve_default=True,
        ),
    ]
