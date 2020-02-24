from celery import Celery
from celery import task 
from celery import shared_task
from django.conf import settings
# We can have either registered task 

celery = Celery('tasks',broker = 'redis://localhost') #!

import os

os.environ[ 'DJANGO_SETTINGS_MODULE' ] = ".settings"


@task(name='printtest') 
def printtest():
    print("testing task") 