from django.db import models
from django.contrib.postgres.fields import JSONField

class Track(models.Model):
    album = models.JSONField()
    artist = models.JSONField()
    available_countries = models.CharField(max_length=100)
    bpm = models.CharField(max_length=100)
    contributors = models.JSONField()
    disk_number = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    explicit_lyrics = models.BooleanField(default=True)
    gain = models.CharField(max_length=100)
    id = models.primary_key(max_length=100)
    isrc = models.CharField(max_length=100)
    link = models.URLField()
    preview = models.URLField()
    rank = models.IntegerField()
    readable = models.CharField(max_length=100)
    release_date = models.CharField(max_length=100)
    share = models.URLField()
    title = models.CharField(max_length=100)
    title_short = models.CharField(max_length=50)
    title_version = models.CharField(max_length=100)
    track_position = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

# Make sure that the first field (error) in CSV is empty
# all IntergerField is in float in Artist.csv
class Artist(models.Model):
    id = models.primary_key(max_length=100)
    link = models.URLField()
    name = models.CharField(max_length=50)
    nb_album models.IntegerField()
    nb_fan = models.IntegerField()
    picture = models.URLField()
    picture_big = models.URLField()
    picture_medium = models.URLField()
    picture_small = models.URLField()
    picture_xl = models.URLField()
    radio = models.BooleanField(default=True)
    share = models.URLField()
    tracklist = models.URLField()
    type = models.CharField(max_length=50)
