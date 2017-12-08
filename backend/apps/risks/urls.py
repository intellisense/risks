from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^risks/$', views.RiskTypeList.as_view(), name='risks_list'),
    url(r'^risks/(?P<pk>[0-9]+)/$', views.RiskTypeDetail.as_view(), name='risk_details'),
    url(r'^fields/$', views.FieldTypes.as_view(), name='field_types'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
