import pandas as pd
from django.shortcuts import render, HttpResponse


facebookDf = pd.read_csv("stubapi/data/facebook.csv")
print(facebookDf.head())

# Create your views here.
def facebook(request):
    fields = request.GET.get("fields", []).split(",")
    start, end = map(int, request.GET.get("rows", "0:10").split(":"))
    response = facebookDf[fields].iloc[start:end, :].to_json()
    return HttpResponse(response, content_type="application/json")
