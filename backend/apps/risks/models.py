# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_noop as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class RiskType(TimeStampedModel):
    class Meta:
        verbose_name = _('Risk Type')
        verbose_name_plural = _('Risk Types')
        ordering = ['-created']

    name = models.CharField(max_length=255)

    @property
    def get_fields_count(self):
        return self.fields.count()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class RiskField(TimeStampedModel):
    class Meta:
        verbose_name = _('Risk Field')
        verbose_name_plural = _('Risk Fields')
        ordering = ['-created']

    TYPE_CHAR = 'char'
    TYPE_INTEGER = 'integer'
    TYPE_DATE = 'date'
    TYPE_SELECT = 'select'

    FIELD_TYPES = (
        (TYPE_CHAR, _('Text Field')),
        (TYPE_INTEGER, _('Integer Field')),
        (TYPE_DATE, _('Date Field')),
        (TYPE_SELECT, _('Dropdown Field')),
    )

    risk_type = models.ForeignKey(RiskType, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(_('Label'), max_length=255)
    field_type = models.CharField(_('Field Type'), max_length=10, choices=FIELD_TYPES, default=TYPE_CHAR)
    required = models.BooleanField(_('Required'), default=True,
                                   help_text=_('Is value for this field required?'))
    help_text = models.CharField(
        _('Help Text'), max_length=255,
        blank=True, default='',
        help_text=_('The help text appears below the field on the form.'
                    ' Use it to clarify what this field means or to give further instructions.'))
    options = models.CharField(
        _('Options'), max_length=255,
        blank=True, default='',
        help_text=_('Comma separated options if field type is Dropdown.'))

    def clean(self):
        if self.field_type:
            if self.field_type == RiskField.TYPE_SELECT:
                if not self.options:
                    raise ValidationError(_('Comma separated options are required when field type is Dropdown.'))
            else:
                self.options = ''
        super(RiskField, self).clean()

    @property
    def get_field_type_name(self):
        return self.get_field_type_display()

    def __str__(self):
        return self.label
