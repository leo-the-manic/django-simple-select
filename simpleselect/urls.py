from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url('^simpleselectquery/$', views.autocomplete_filter, name='simpleselect'),
)
