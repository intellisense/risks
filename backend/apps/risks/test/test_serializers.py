# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import copy

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..models import RiskField, RiskType
from ..serializers import RiskFieldSerializer, RiskTypeSerializer


class TestRiskFieldSerializer(TestCase):
    def setUp(self):
        self.risk_type = RiskType.objects.create(name='test')
        self.risk_field_data = {
            'risk_type': self.risk_type,
            'field_type': RiskField.TYPE_CHAR,
            'label': 'char'
        }
        self.risk_field = RiskField.objects.create(**self.risk_field_data)
        self.serializer = RiskFieldSerializer(instance=self.risk_field)

    def test_sanity(self):
        self.assertEqual(
            set(self.serializer.data.keys()),
            {'field_type', 'label', 'name', 'help_text', 'required', 'id', 'options'}
        )

    def test_field_type(self):
        data = self.serializer.data
        self.assertEqual(data['field_type'], self.risk_field_data['field_type'])

    def test_label(self):
        data = self.serializer.data
        self.assertEqual(data['label'], self.risk_field_data['label'])

    def test_name(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.risk_field.get_field_type_display())

    def test_help_text(self):
        data = self.serializer.data
        self.assertEqual(data['help_text'], '')

    def test_required(self):
        data = self.serializer.data
        self.assertTrue(data['required'])

    def test_options(self):
        data = self.serializer.data
        self.assertEqual(data['options'], '')


class TestRiskTypeSerializer(TestCase):
    def setUp(self):
        self.risk_type_name = 'test'
        self.risk_type = RiskType.objects.create(name=self.risk_type_name)
        self.risk_field_data = {
            'risk_type': self.risk_type,
            'field_type': RiskField.TYPE_CHAR,
            'label': 'char'
        }
        self.risk_field = RiskField.objects.create(**self.risk_field_data)
        self.serializer = RiskTypeSerializer(instance=self.risk_type)
        self.test_data = {
            'name': 'new test',
            'fields': [
                {
                    'id': 0,  # serializer will `update` and `create` will discard this.
                    'field_type': RiskField.TYPE_CHAR,
                    'label': 'char',
                    'help_text': 'this is a test',
                    'required': False,
                    'options': 'dummy'
                }
            ]
        }

    def test_sanity(self):
        self.assertEqual(
            set(self.serializer.data.keys()),
            {'id', 'name', 'fields', 'fields_count', 'created', 'modified'}
        )

    def test_name(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.risk_type_name)

    def test_fields_count_in_data(self):
        data = self.serializer.data
        self.assertEqual(len(data['fields']), 1)

    def test_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data['fields'][0].keys()),
            {'field_type', 'label', 'name', 'help_text', 'required', 'id', 'options'}
        )

    def test_fields_count(self):
        data = self.serializer.data
        self.assertEqual(data['fields_count'], 1)

    def test_created(self):
        data = self.serializer.data
        self.assertEqual(data['created'], self.risk_type.created.strftime(RiskTypeSerializer.DATE_TIME_FORMAT))

    def test_modified(self):
        data = self.serializer.data
        self.assertEqual(data['modified'], self.risk_type.created.strftime(RiskTypeSerializer.DATE_TIME_FORMAT))

    def test_valid_creation(self):
        serializer = RiskTypeSerializer(data=self.test_data)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.name, self.test_data['name'])
        self.assertEqual(obj.get_fields_count, 1)
        field = obj.fields.first()
        field_data = self.test_data['fields'][0]
        self.assertEqual(field.field_type, field_data['field_type'])
        self.assertEqual(field.label, field_data['label'])
        self.assertEqual(field.help_text, field_data['help_text'])
        self.assertEqual(field.required, field_data['required'])
        self.assertEqual(field.options, '')

    def test_valid_update(self):
        # with addition of new risk field and removal of older one
        serializer = RiskTypeSerializer(data=self.test_data, instance=self.risk_type)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, self.risk_type.id)
        self.assertEqual(obj.get_fields_count, 1)
        self.assertNotEqual(obj.name, self.risk_type_name)
        new_field = obj.fields.first()
        self.assertNotEqual(new_field.id, self.risk_field.id)

        # no new field created when id present
        data = copy.deepcopy(self.test_data)
        data['fields'][0]['id'] = new_field.id
        serializer = RiskTypeSerializer(data=data, instance=self.risk_type)
        self.assertTrue(serializer.is_valid())
        obj = serializer.save()
        self.assertEqual(obj.id, self.risk_type.id)
        self.assertEqual(obj.get_fields_count, 1)
        field = obj.fields.first()
        self.assertEqual(field.id, new_field.id)

    def test_invalid(self):
        data = copy.deepcopy(self.test_data)

        # missing risk type name
        data['name'] = ''
        serializer = RiskTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        # missing fields
        data['name'] = self.test_data['name']
        data['fields'] = []
        serializer = RiskTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        # invalid field data
        data['fields'] = copy.copy(self.test_data['fields'])
        data['fields'][0]['field_type'] = 'invalid'
        serializer = RiskTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
