# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views import generic
from django.utils import simplejson
from main.models import Servers, AlertHistories,Processes
from django.conf import settings


import urllib2
import base64
from urlparse import urlparse
import sys
import re

import simplejson as json
from chartit import DataPool,Chart

def base_url(request):
    base_url = settings.BASE_URL
    return {'BASE_URL': base_url}


def index(request):

    alerthistories=AlertHistories.objects.all().order_by('subject')
    c={'alerthistories':alerthistories}
    servers=Servers.objects.all().order_by('nickname')
    d={'servers':servers}


    stackedchart = \
        DataPool(
           series=
            [{'options': {
               'source': Processes.objects.all()},
              'terms': [
                'time',
                'cpu_data',
                'memory_data']}
             ])


    cht = Chart(
            datasource = stackedchart,
            series_options =
              [{'options':{
                  'type': 'bar',
                  'stacking': True},
                'terms':{
                  'time': [
                    'cpu_data',
                    ]
                  }}],
            chart_options =
              {'title': {
                   'text': 'Process Visualisation'},
               'xAxis': {
                    'title': {
                       'text': 'Time'}}})


    return render_to_response('index.html',
                          c,d,{'stackedchart': cht},
                          context_instance=RequestContext(request))

def api_servers(request):
    url = settings.BASE_URL + "servers/"
    return api_get_data(url)


def api_alert_histories(request):
    url = settings.BASE_URL + "alert-histories/?num=50/"
    return api_get_data(url)


def api_processes(request):
    url = settings.BASE_URL + 'servers/' + request.GET.get('id') + '/processes/?start=' + request.GET.get(
        'start') + '&end=' + request.GET.get('end')
    return api_get_data(url)


def api_process_data(request):
    url = settings.BASE_URL + 'processes/' + request.GET.get('uid') + '/data/'
    return api_get_data(url)


def api_get_data(url):
    base64string = base64.encodestring('%s:%s' % (settings.USERNAME, settings.API_KEY))[:-1]
    authheader = "Basic %s" % base64string
    req = urllib2.Request(url)
    req.add_header("Authorization", authheader)
    try:
        handle = urllib2.urlopen(req)
    except IOError, e:
        sys.exit(1)
    return_data = handle.read()
    data = json.loads(return_data)
    servers=Servers.objects.create(nickname=data['nickname'],id=data['id'])
    alerthistories = AlertHistories.objects.create(subject=data['subject'], start=data['start'],end=data['end'])
    processes= Processes.objects.create(uid=data['uid'],cpu=data['cpu'],memory=data['memory'])
    if 'alert-histories' in data:
        alerts = data['alerts']
        for alert in alerts:
            w = AlertHistories.objects.get_or_create(**alert)
            alerthistories.alert.add(w)

    if 'servers' in data:
        servers = data['servers']
        for server in servers:
            w = Servers.objects.get_or_create(**server)
            servers.server.add(w)

    return HttpResponse(return_data, mimetype="application/json")




