import pandas as pd
from django.shortcuts import render, HttpResponse


facebookDf = pd.read_csv("stubapi/data/facebook.csv")
print(facebookDf.head())

# Create your views here.
def facebook(request):
    fields = request.GET.get("fields", []).split(",")
    response = facebookDf[fields].to_json()
    return HttpResponse(response, content_type="application/json")
