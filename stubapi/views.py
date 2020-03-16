import pandas as pd
from django.shortcuts import render, HttpResponse


smdf1 = pd.read_csv("stubapi/data/sm1.csv")
smdf2 = pd.read_csv("stubapi/data/sm2.csv")
print(smdf1.head())
print(smdf2.head())

# http://127.0.0.1:8000/stubapi/sm1/?fields=ad_id,reporting_start,impressions,age,spent&rows=0:10
# http://127.0.0.1:8000/stubapi/sm2/?fields=ad_id,start_date,impressions,age,cost&rows=0:20

# Create your views here.
def sm1(request):
    fields = request.GET.get("fields", []).split(",")
    start, end = map(int, request.GET.get("rows", "0:10").split(":"))
    response = smdf1[fields].iloc[start:end, :].to_json()
    return HttpResponse(response, content_type="application/json")


def sm2(request):
    fields = request.GET.get("fields", []).split(",")
    start, end = map(int, request.GET.get("rows", "0:10").split(":"))
    response = smdf2[fields].iloc[start:end, :].to_json()
    return HttpResponse(response, content_type="application/json")
