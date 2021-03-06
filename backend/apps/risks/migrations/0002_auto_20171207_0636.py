# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-07 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='riskfieldoption',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='riskfieldoption',
            name='risk_field',
        ),
        migrations.AddField(
            model_name='riskfield',
            name='options',
            field=models.CharField(blank=True, default='', help_text='Comma separated options if field type is Dropdown.', max_length=255, verbose_name='Options'),
        ),
        migrations.AlterField(
            model_name='riskfield',
            name='field_type',
            field=models.CharField(choices=[('char', 'Text Field'), ('integer', 'Integer Field'), ('date', 'Date Field'), ('select', 'Dropdown Field')], default='char', max_length=10, verbose_name='Field Type'),
        ),
        migrations.AlterField(
            model_name='riskfield',
            name='help_text',
            field=models.CharField(blank=True, default='', help_text='The help text appears below the field on the form. Use it to clarify what this field means or to give further instructions.', max_length=255, verbose_name='Help Text'),
        ),
        migrations.DeleteModel(
            name='RiskFieldOption',
        ),
    ]
