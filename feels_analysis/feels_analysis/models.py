from django.db import models
from model_utils.models import TimeStampedModel

class Track(TimeStampedModel):
    track_name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)

    track_id = models.IntegerField(unique=True, null=True)
    lyrics = models.TextField(blank=True)

    neg = models.FloatField(null=True)
    neu = models.FloatField(null=True)
    pos = models.FloatField(null=True)

    # removes a certain but of a disclaimer that messes with the lyrics
    def stripDisclaimer(self):
        new_lyrics = self.lyrics.strip("... ******* This Lyrics is NOT for Commercial use *******")
        self.lyrics = new_lyrics
        self.save()
    # CS112 level coding up in here
    def mood(self):
        data = [self.neg, self.neu, self.pos]
        largest = max(data)
        indexlargest = data.index(largest)
        if indexlargest == 0:
            mood = 'Negative'
        elif indexlargest == 1:
            mood = 'Neutral'
        else:
            mood = 'Positive'
        return (mood, largest)
    def __str__(self):
        return self.track_name

    def __unicode__(self):
        return unicode(self.track_name)
