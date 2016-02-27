from __future__ import absolute_import, print_function

from .models import *

from django.conf import settings
from django.http import HttpResponseServerError  # Http404
from django.shortcuts import render, get_object_or_404, redirect

import requests, json

def index(request):
    payload = {
        "api_key": 'REDACETED',
        "method": 'chart.getTopTracks',
        "limit": '1',
        "format": 'json' }
    r = requests.get('http://ws.audioscrobbler.com/2.0/', params=payload)
    return render(request, 'index.html', {
        'data0': r.json()["tracks"]["track"][0]["name"],
        'data': r.json()["tracks"]["track"][0]["artist"]["name"]
    },)
