from django.contrib import admin
from .models import *


class TrackAdmin(admin.ModelAdmin):
    list_display = ("track_name", "artist", "track_id", "lyrics")


admin.site.register(Track, TrackAdmin)
