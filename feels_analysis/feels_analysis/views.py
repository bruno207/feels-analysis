from __future__ import absolute_import

from .models import *

from django.conf import settings
from django.http import HttpResponseServerError  # Http404
from django.shortcuts import render, get_object_or_404, redirect

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

import requests, json

def index(request):
    # Last.fm Track API requests
    num_tracks = 10
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


    def getTrackId(artist, track):
        # Musixmatch Track ID API requests
        payload = {
            "apikey": 'REDACTED',
            "method": 'track.search',
            "q_track": '%s' %track,
            "q_artist": "'{0}'".format(artist),
            "f_has_lyrics": '1',
            "format": 'json',
            "page_size": '1',
        }
        r = requests.get('http://api.musixmatch.com/ws/1.1/', params=payload)
        return r.json()["message"]["body"]["track_list"][0]["track"]["track_id"]

    def getTrackLyrics(track_id):
        # Musixmatch Lyrics API requests
        payload = {
            "apikey": 'REDACTED',
            "method": 'track.lyrics.get',
            "format": 'json',
            "track_id": '%s' %track_id,
        }
        r = requests.get('http://api.musixmatch.com/ws/1.1/', params=payload)
        return r.json()["message"]["body"]["lyrics"]["lyrics_body"]

    # API data processing into the databse logic:
    for i in range(len(topTracks)):
        curr_track_name = topTracks[i][1]
        curr_artist = topTracks[i][0]
        # Prevent unnecessary api calls to musixmatch
        obj, created = Track.objects.get_or_create(track_name=curr_track_name, artist=curr_artist)
        if created:
            curr_track_id = getTrackId(curr_artist, curr_track_name)
            curr_lyrics = getTrackLyrics(curr_track_id)
            obj.track_id = curr_track_id
            obj.lyrics = curr_lyrics
            obj.save()

    # placeholder for pretty page
    test = 'no errors'
    return render(request, 'index.html', {
        'data': test,
    },)
