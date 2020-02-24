from celery import shared_task, task
from django.contrib.auth.models import User
from django.contrib.auth.models import CeleryScheduler


@shared_task
def fetch_data():
    print("test passed ")
    users = User.objects.all()
    print(users)
    # query for fetching all the

