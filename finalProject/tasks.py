from celery import task 
from celery import shared_task 
# We can have either registered task 
@task(name='summary') 
def send_import_summary():
    print('testing')