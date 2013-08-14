# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views import generic
from django.utils import simplejson
from main.models import Servers, AlertHistories
from django.conf import settings

import urllib2
import base64
from urlparse import urlparse
import sys
import re

import simplejson as json


def base_url(request):
    base_url = settings.BASE_URL
    return {'BASE_URL': base_url}


def index(request):
    stackedchart = []
    stackedchart.append({
            "id" : 1,
            "ProcessData":[],
            "timerInterval": 1,
            "Servers":[],

            "timerIntervalCounter": 0
            })

    return render_to_response("../templates/index.html",{"stackedchart":stackedchart}, context_instance = RequestContext(request))


def api_servers(request):
    url = settings.BASE_URL + "servers/"
    return api_get_data(url)


def api_alert_histories(request):
    url = settings.BASE_URL + "alert-histories/?num=5000/"
    return api_get_data(url)


def api_processes(request):
        url = settings.BASE_URL + 'servers/' + request.GET.get('id') + '/processes/?start='+request.GET.get('start')+'&end='+request.GET.get('end')
        return api_get_data(url)


def api_process_data(request):
        url = settings.BASE_URL + 'processes/' + request.GET.get('uid') + '/data/'
        return api_get_data(url)


def api_get_data(url):
    base64string = base64.encodestring('%s:%s' %(settings.USERNAME,settings.API_KEY))[:-1]
    authheader = "Basic %s" % base64string
    req = urllib2.Request(url)
    req.add_header("Authorization", authheader)
    try:
        handle = urllib2.urlopen(req)
    except IOError, e:
        sys.exit(1)
    return_data = handle.read()
    return HttpResponse(return_data ,mimetype="application/json")
