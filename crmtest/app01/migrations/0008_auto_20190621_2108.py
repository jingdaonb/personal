# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-06-21 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20190621_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to='app01.UserInfo', verbose_name='老师'),
        ),
        migrations.AlterField(
            model_name='classstudyrecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='讲师'),
        ),
        migrations.AlterField(
            model_name='consultrecord',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='app01.UserInfo', verbose_name='跟进人'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='销售'),
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(to='app01.Permission'),
        ),
    ]
