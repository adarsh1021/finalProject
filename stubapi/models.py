from django.db import models
from datetime import datetime

# Create your models here.
import random


def randomVal(l=0, k=50):
    return random.randrange(l, k)


# id,title,description,image,campaign_id,date,likes_count,shares_count,views,clicks,cost
class Facebook(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default=None)
    description = models.TextField()
    image = models.CharField(max_length=500, default=None)
    campaign_id = models.IntegerField(default=124612)
    date = models.DateTimeField(default=datetime.now, blank=True)
    likes_count = models.IntegerField(default=lambda: randomVal(15, 50))
    shares_count = models.IntegerField(default=lambda: randomVal(2, 20))
    views = models.IntegerField(default=lambda: randomVal(20, 100))
    clicks = models.IntegerField(default=lambda: randomVal(20, 50))
    cost = models.DecimalField(
        default=lambda: randomVal(10, 100) * 0.1,
        max_digits=10,
        decimal_places=2,
    )


# id,title,description,image,campaign_id,date,heart_count,retweets_count,impressions,clicks,cost
class Twitter(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default=None)
    description = models.TextField()
    image = models.CharField(max_length=500, default=None)
    campaign_id = models.IntegerField(default=1123)
    date = models.DateTimeField(default=datetime.now, blank=True)
    heart_count = models.IntegerField(default=lambda: randomVal(15, 50))
    retweets_count = models.IntegerField(default=lambda: randomVal(2, 20))
    impressions = models.IntegerField(default=lambda: randomVal(20, 100))
    clicks = models.IntegerField(default=lambda: randomVal(20, 50))
    cost = models.DecimalField(
        default=lambda: randomVal(10, 100) * 0.1,
        max_digits=10,
        decimal_places=2,
    )
