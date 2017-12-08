# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from ..models import RiskType, RiskField
from ..serializers import RiskTypeSerializer


class TestRiskTypeListView(APITestCase):
    def setUp(self):
        self.records = 5
        for i in range(self.records):
            obj = RiskType.objects.create(name='test')
            risk_field_data = {
                'risk_type': obj,
                'field_type': RiskField.TYPE_CHAR,
                'label': 'char'
            }
            RiskField.objects.create(**risk_field_data)
        self.data = {'name': 'test', 'fields': [{'label': 'test', 'field_type': RiskField.TYPE_CHAR, 'id': 0}]}
        self.invalid_payload = {'name': '', 'fields': [{'label': 'test', 'field_type': RiskField.TYPE_CHAR, 'id': 0}]}
        self.endpoint = reverse('api:risks_list')
        self.api_client = APIClient()

    def test_list(self):
        response = self.api_client.get(self.endpoint)
        qs = RiskType.objects.all()
        serializer = RiskTypeSerializer(qs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        response = self.api_client.post(self.endpoint, data=self.data, format='json')
        self.assertEqual(RiskType.objects.count(), self.records+1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_failed(self):
        response = self.api_client.post(self.endpoint, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_allowed_put(self):
        response = self.api_client.put(self.endpoint, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_patch(self):
        response = self.api_client.patch(self.endpoint, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_delete(self):
        response = self.api_client.patch(self.endpoint, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestRiskTypeDetailView(APITestCase):
    def setUp(self):
        self.risk_type = RiskType.objects.create(name='test')
        risk_field_data = {
            'risk_type': self.risk_type,
            'field_type': RiskField.TYPE_CHAR,
            'label': 'char'
        }
        self.risk_field = RiskField.objects.create(**risk_field_data)
        self.endpoint = reverse('api:risk_details', args=(self.risk_type.id, ))
        self.api_client = APIClient()

    def test_retrieve(self):
        response = self.api_client.get(self.endpoint)
        serializer = RiskTypeSerializer(instance=self.risk_type)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_404(self):
        endpoint = reverse('api:risk_details', args=(0, ))
        response = self.api_client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        # get API response
        data = {'name': 'new test', 'fields': [{'label': 'test', 'field_type': RiskField.TYPE_DATE, 'id': 0}]}
        response = self.api_client.patch(self.endpoint, data=data, format='json')
        # refresh from db
        obj = RiskType.objects.get(id=self.risk_type.id)
        serializer = RiskTypeSerializer(instance=obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(obj.name, data['name'])
        self.assertEqual(obj.get_fields_count, 1)
        field = obj.fields.first()
        self.assertEqual(field.label, data['fields'][0]['label'])
        self.assertEqual(field.field_type, data['fields'][0]['field_type'])

    def test_update_failed(self):
        data = {'name': '', 'fields': [{'label': 'test', 'field_type': RiskField.TYPE_DATE, 'id': 0}]}
        response = self.api_client.patch(self.endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        response = self.api_client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RiskType.objects.count(), 0)
        self.assertEqual(RiskField.objects.count(), 0)

    def test_not_allowed_post(self):
        response = self.api_client.post(self.endpoint, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestFieldTypesView(APITestCase):
    def setUp(self):
        self.endpoint = reverse('api:field_types')
        self.api_client = APIClient()

    def test_get(self):
        data = [{'field_type': k, 'name': v} for k, v in RiskField.FIELD_TYPES]
        response = self.api_client.get(self.endpoint)
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_allowed_post(self):
        response = self.api_client.post(self.endpoint, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_put(self):
        response = self.api_client.put(self.endpoint, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_patch(self):
        response = self.api_client.patch(self.endpoint, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_allowed_delete(self):
        response = self.api_client.patch(self.endpoint, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
