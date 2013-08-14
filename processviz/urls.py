from django.conf.urls import patterns, include, url
from main import views
import os.path
from django.conf.urls import *

static = os.path.join(
    os.path.dirname(__file__),'static'
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',views.index,name="index"),
    url(r'^index/', views.index),

    url(r'^api/server/process/', views.api_processes, name="processes"),
    url(r'^api/process/data/$', views.api_process_data, name="process_data"),
    url(r'^api/server/$', views.api_servers, name = "servers"),
    url(r'^api/alert-histories/$',views.api_alert_histories,name="alert_histories"),
    # Examples:
    # url(r'^$', 'processviz.views.home', name='home'),
    # url(r'^processviz/', include('processviz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
