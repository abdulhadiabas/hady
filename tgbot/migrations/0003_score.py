# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-26 09:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_auto_20170125_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='امتیاز')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='tgbot.People', verbose_name='بازیکن')),
                ('record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='points', to='tgbot.Record', verbose_name='رکورد')),
            ],
            options={
                'verbose_name_plural': 'امتیازها',
                'ordering': ('-creation_time',),
                'verbose_name': 'امتیاز',
            },
        ),
    ]