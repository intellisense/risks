# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import RiskType, RiskField
from .serializers import RiskTypeSerializer


class RiskTypeList(generics.ListCreateAPIView):
    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer


class RiskTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer


class FieldTypes(APIView):
    def get(self, request, **kwargs):
        """
        Return a list of RiskField.FIELD_TYPES.
        """
        data = [{'field_type': k, 'name': v} for k, v in RiskField.FIELD_TYPES]
        return Response(data)
