from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
import pandas as pd


class CustomTable(models.Model):
    """
    id
    tableName
    tableStructure
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    structure = JSONField()

    def get_df(self):
        campaign1, campaign2 = self.structure
        fields1, fields2 = self.structure[campaign1], self.structure[campaign2]

        df1_fields_map = {}
        df2_fields_map = {}

        for fIdx in range(len(fields1)):
            if fields1[fIdx] != fields2[fIdx]:
                # perform type casting
                df1_fields_map[
                    fields1[fIdx]
                ] = f"{fields1[fIdx]}__{fields2[fIdx]}"
                df2_fields_map[
                    fields2[fIdx]
                ] = f"{fields1[fIdx]}__{fields2[fIdx]}"
            else:
                df1_fields_map[fields1[fIdx]] = fields1[fIdx]
                df2_fields_map[fields2[fIdx]] = fields2[fIdx]

        df1 = Data.objects.filter(campaign__id=campaign1).order_by(
            "-created_at"
        )[0]
        df1 = pd.DataFrame(df1.data)
        df2 = Data.objects.filter(campaign__id=campaign2).order_by(
            "-created_at"
        )[0]
        df2 = pd.DataFrame(df2.data)

        # output table
        finalDf = pd.concat(
            [
                df1.rename(columns=df1_fields_map),
                df2.rename(columns=df2_fields_map),
            ],
            ignore_index=True,
        )

        return finalDf


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
    # socialMedia - sm
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    crawlInterval = models.IntegerField(choices=CRAWL_INTERVAL_OPTIONS)
    fields = JSONField()


class Data(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()
