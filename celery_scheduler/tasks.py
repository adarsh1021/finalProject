from celery import shared_task, task
from django.contrib.auth.models import User
from celery_scheduler.models import CeleryScheduler
from backend.models import Data


@shared_task
def fetch_data():
    print("test passed ")
    users = User.objects.all()
    print(users)

    schedules_to_rn = CeleryScheduler.objects.filter(date_time)

    for schedule in schedules_to_rn:
        data = fetch(schedule.endpoint)
        Data.create(campaign=schedule.id, data=data)

