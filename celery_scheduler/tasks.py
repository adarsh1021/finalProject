from celery import shared_task, task
from django.contrib.auth.models import User
from backend.models import Campaign
from backend.models import Data
from datetime import date
import urllib2
import json


@shared_task
def fetch_data():
    print("test passed ")
    # users = User.objects.all()
    # print(users)

    daily_campaigns = Campaign.objects.filter(crawlInterval=Campaign.DAILY)

    for campaign in daily_campaigns:
        response=urllib2.urlopen(campaign.source)
        data=json.load(response)
        Data.create(campaign=campaign, data=data)

