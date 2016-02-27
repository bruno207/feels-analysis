from django.db import models
from model_utils.models import TimeStampedModel

class Track(TimeStampedModel):
    track_name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)

    track_id = models.IntegerField(unique=True, null=True)
    lyrics = models.TextField(blank=True)

    def stripDisclaimer(self):
        new_lyrics = self.lyrics.strip("... ******* This Lyrics is NOT for Commercial use *******")
        self.lyrics = new_lyrics
        self.save()

    def __str__(self):
        return self.track_name

    def __unicode__(self):
        return unicode(self.track_name)
