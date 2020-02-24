from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


# class CustomTable(models.Model):
#     """
#     id
#     source
#     tableName
#     tableStructure
#     """

#     SOURCE_TYPE_OPTIONS = (
#         ("csv", "CSV"),
#         ("api", "API"),
#         ("ct", "CustomTable"),
#     )
#     sourceType = models.CharField(
#         max_length=5, choices=SOURCE_TYPE_OPTIONS, default="api"
#     )
#     # Source can be different depending upon sourceType
#     # fileName - csv
#     # apiID - api
#     # customTableId - ct
#     source = models.CharField(max_length=256)
#     name = models.CharField(max_length=100)
#     fields = JSONField()


class Campaign(models.Model):
    """ 
    id
    customTable
    startDate
    crawlInterval
    lastUpdate (timestamp)
    """

    DAILY = 1440
    WEEKLY = 10080
    MONTHLY = 43800
    # interval in minutes
    CRAWL_INTERVAL_OPTIONS = (
        (DAILY, "daily"),
        (WEEKLY, "weekly"),
        (MONTHLY, "monthly"),
    )

    SOURCE_TYPE_OPTIONS = (
        ("csv", "CSV"),
        ("api", "API"),
        ("sm", "Social Media")
        # ("ct", "CustomTable"), # Maybe do this later - dont need this level of complexity now
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    sourceType = models.CharField(
        max_length=5, choices=SOURCE_TYPE_OPTIONS, default="api"
    )
    # Source can be different depending upon sourceType
    # fileName - csv
    # apiID - api
    # customTableId - ct
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    crawlInterval = models.IntegerField(choices=CRAWL_INTERVAL_OPTIONS)
    fields = JSONField()


class Data(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()
