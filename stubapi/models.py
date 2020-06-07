from django.db import models
from datetime import datetime

# Create your models here.


class Facebook(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    campaign_id = models.IntegerField(default=1123)
    date = models.DateTimeField(default=datetime.now, blank=True)
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    cost = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)


class Twitter(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    campaign_id = models.IntegerField(default=1123)
    date = models.DateTimeField(default=datetime.now, blank=True)
    likes_count = models.IntegerField(default=0)
    retweets_count = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    cost = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
