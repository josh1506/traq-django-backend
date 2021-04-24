from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Url(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='url')
    title = models.CharField(max_length=25, blank=False)
    link = models.URLField(max_length=255, blank=False)
    short_url = models.CharField(max_length=20)

    def total_visitors(self):
        return len(self.viewer.all())

    def __str__(self):
        return self.title


class Viewer(models.Model):
    url = models.ForeignKey(
        Url, on_delete=models.CASCADE, related_name='viewer')
    date_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url.title

    def __lt__(self, other):
        return self.date_viewed < other.date_viewed
