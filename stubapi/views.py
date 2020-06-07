from rest_framework import generics
from rest_framework.response import Response
from django_filters import rest_framework as filters
import pandas as pd

from django.shortcuts import render, HttpResponse

from .models import Facebook, Twitter
from .serializers import FacebookSerializer

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


def facebook(request):
    return render(request, "facebook.html")


class facebook_api(generics.ListAPIView):
    queryset = Facebook.objects.all()
    serializer_class = FacebookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["id", "campaign_id", "date"]

    def post(self, request):
        obj = FacebookSerializer(data=request.data)
        obj.is_valid()
        obj.save()
        return Response(status=200)


# class InvoiceAPIView(APIView):
#     def post(self, request):
#         serializer = InvoiceSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=request.user, status=Invoice.SENT)
#         return Response(status=status.HTTP_201_CREATED)
