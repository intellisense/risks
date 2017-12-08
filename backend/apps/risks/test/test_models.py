# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..models import RiskType, RiskField


class TestRiskType(TestCase):
    def test_valid(self):
        o = RiskType.objects.create(name='test')
        self.assertEqual(o.name, 'test')
        self.assertEqual(o.get_fields_count, 0)
        self.assertGreater(timezone.now(), o.created)
        self.assertGreater(timezone.now(), o.modified)

    def test_invalid(self):
        with self.assertRaises(ValidationError):
            o = RiskType(name='')
            o.full_clean()


class TestRiskField(TestCase):
    def setUp(self):
        self.risk_type = RiskType.objects.create(name='test')

    def test_valid(self):
        o = RiskField.objects.create(
            risk_type=self.risk_type,
            field_type=RiskField.TYPE_CHAR,
            label='char'
        )
        self.assertEqual(o.risk_type_id, self.risk_type.id)
        self.assertEqual(o.field_type, RiskField.TYPE_CHAR)
        self.assertEqual(o.label, 'char')
        self.assertEqual(self.risk_type.get_fields_count, 1)
        self.assertGreater(timezone.now(), o.created)
        self.assertGreater(timezone.now(), o.modified)

    def test_invalid(self):
        # invalid `field_type`
        with self.assertRaises(ValidationError):
            o = RiskField(
                risk_type=self.risk_type,
                field_type='invalid',
                label='char'
            )
            o.full_clean()

        # no `label`
        with self.assertRaises(ValidationError):
            o = RiskField(
                risk_type=self.risk_type,
                field_type=RiskField.TYPE_CHAR,
            )
            o.full_clean()

        # no `risk_type`
        with self.assertRaises(ValidationError):
            o = RiskField(
                field_type=RiskField.TYPE_CHAR,
                label='char'
            )
            o.full_clean()

        # no `risk_type`
        with self.assertRaises(IntegrityError):
            RiskField.objects.create(
                field_type=RiskField.TYPE_CHAR,
                label='char'
            )

    def test_no_options(self):
        """
        Only field of type `RiskField.TYPE_SELECT` can have options
        """
        for t in RiskField.FIELD_TYPES:
            field_type = t[0]
            o = RiskField.objects.create(
                risk_type=self.risk_type,
                field_type=field_type,
                label='test',
                options='test'
            )
            o.full_clean()
            if field_type != RiskField.TYPE_SELECT:
                self.assertEqual(o.options, '')
            else:
                self.assertEqual(o.options, 'test')
