from django.conf.urls import include
from django.urls import re_path as url

from ansaotuvi_website.views import ansaotuvi_website_index, api

urlpatterns = [
    url(r'^api', api),
    url(r'^$', ansaotuvi_website_index)
]