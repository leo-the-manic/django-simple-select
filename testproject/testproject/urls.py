from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    ('^', include('simpleselect.urls')),
    ('^', include('demo.urls')),
)
