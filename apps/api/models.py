from django.db import models

class GeoLocation(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=100)

class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField()
    subtitle = models.CharField()
    content = models.TextField()
    date = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)
    locations = models.ManyToManyField(GeoLocation)
    personas = models.ManyToManyField(Persona)
