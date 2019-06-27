from django.conf.urls import url, include
from django.contrib import admin
from . import views
from apps.login.urls import urlpatterns

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^infopage/(?P<parkid>\d+)$', views.parkinfo),
]
