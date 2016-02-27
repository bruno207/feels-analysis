# Python 3 imports
from __future__ import absolute_import
# import from db
from .models import *
# django imports
from django.conf import settings
from django.shortcuts import render
# external app imports
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import requests

def index(request):
    # Last.fm Track API requests
    num_tracks = 99
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

    def determineSentiment(track_lyrics):
        # VADER Sentiment calculatrion and database storage
        try:
            track_lyrics = track_lyrics.encode('utf-8')
            sentiment = vaderSentiment(track_lyrics)
        except UnicodeEncodeError:
            track_lyrics = track_lyrics.encode('ascii', 'ignore')
            sentiment = vaderSentiment(track_lyrics)
        neg = sentiment['neg']
        neu = sentiment['neu']
        pos = sentiment['pos']
        return (neg,neu,pos)

    # API data processing into the databse logic:
    for i in range(len(topTracks)):
        curr_track_name = topTracks[i][1]
        curr_artist = topTracks[i][0]
        # Prevent Macklemore from being input multiple time (TODO investigate)
        if Track.objects.get(track_id='84285276'):
            continue
        # Prevent unnecessary api calls to musixmatch
        obj, created = Track.objects.get_or_create(track_name=curr_track_name, artist=curr_artist)
        if created:
            try:
                curr_track_id = getTrackId(curr_artist, curr_track_name)
                curr_lyrics = getTrackLyrics(curr_track_id)
                obj.track_id = curr_track_id
                obj.lyrics = curr_lyrics
                obj.stripDisclaimer()
                sentiment = determineSentiment(obj.lyrics)
                obj.neg, obj.neu, obj.pos = sentiment
                obj.save()
            except:
                print curr_artist
                continue

    test = "There are no errors!"
    return render(request, 'index.html', {
        'data': test,
    },)
