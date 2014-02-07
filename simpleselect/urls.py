from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url('^simpleselectquery/$', views.autocomplete_filter,
        name='simpleselect'),
)
