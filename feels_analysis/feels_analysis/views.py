from __future__ import absolute_import, print_function

from .models import *

from django.conf import settings
from django.http import HttpResponseServerError  # Http404
from django.shortcuts import render, get_object_or_404, redirect

import requests, json

def index(request):
    num_tracks = 1
    # topTracks = {}
    payload = {
        "api_key": 'REDACTED',
        "method": 'geo.getTopTracks',
        "country": 'United States',
        "limit": '%s' %num_tracks,
        "format": 'json',
    }
    r = requests.get('http://ws.audioscrobbler.com/2.0/', params=payload)

    topTracks = [(r.json()["tracks"]["track"][num]["artist"]["name"],
                  r.json()["tracks"]["track"][num]["name"])
                 for num in range(num_tracks)]

    return render(request, 'index.html', {
        'data': r.json(),
    },)
