from django.db import models
from model_utils.models import TimeStampedModel

class Track(TimeStampedModel):
    track_name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)

    track_id = models.IntegerField(default=0)
    lyrics = models.TextField(blank=True)

    def __str__(self):
        return self.track_name

    def __unicode__(self):
        return unicode(self.track_name)
