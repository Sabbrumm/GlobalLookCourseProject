from django.db import models
from django.contrib.auth.models import User

from apps.api.models import GeoLocation, Persona


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField()
    subtitle = models.CharField()
    content = models.TextField()
    date = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)
    locations = models.ManyToManyField(GeoLocation)
    personas = models.ManyToManyField(Persona)
