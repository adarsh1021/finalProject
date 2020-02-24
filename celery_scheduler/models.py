from django.db import models

# Create your models here.


class CeleryScheduler(models.Model):
    """
    schedule - daily, weekly, monthly
    endpoint - https:/// ....
    target - table name
    """
    schedule = models.CharField(max_length=30)
    endpoint = models.CharField(max_length=200)
    target_table = models.CharField(max_length=50)

