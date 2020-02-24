from celery import Celery
from celery import task 
from celery import shared_task
from django.conf import settings
# We can have either registered task 

celery = Celery('tasks',broker = 'redis://localhost:6379') #!

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalProject.settings')
app = Celery('finalProject')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = 'UTC'

@app.task(name='printtest') 
def printtest():
    print("testing task") 