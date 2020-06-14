from rest_framework import generics
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

from django.shortcuts import render, HttpResponse

from .models import Facebook, Twitter
from .serializers import FacebookSerializer, TwitterSerializer

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


@csrf_exempt
def facebook(request):
    if request.method == "GET":
        posts = Facebook.objects.all().order_by("-date")
        return render(request, "facebook.html", {"posts": posts})
    elif request.method == "POST":
        print(request.POST)
        if request.POST.get("like"):
            obj = Facebook.objects.get(id=request.POST.get("post_id"))
            obj.likes_count += 1
            obj.save()
            print("like")
        elif request.POST.get("share"):
            obj = Facebook.objects.get(id=request.POST.get("post_id"))
            obj.shares_count += 1
            obj.save()
            print("share")
        return JsonResponse({"msg": "success"})


def twitter(request):
    if request.method == "GET":
        posts = Twitter.objects.all().order_by("-date")
        return render(request, "twitter.html", {"posts": posts})
    elif request.method == "POST":
        print(request.POST)
        if request.POST.get("retweet"):
            obj = Twitter.objects.get(id=request.POST.get("tweet_id"))
            obj.retweets_count += 1
            obj.save()
            print("like")
        elif request.POST.get("like"):
            obj = Twitter.objects.get(id=request.POST.get("tweet_id"))
            obj.likes_count += 1
            obj.save()
            print("retweet")
        return JsonResponse({"msg": "success"})


class facebook_api(generics.ListAPIView):
    queryset = Facebook.objects.all()
    serializer_class = FacebookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["id", "campaign_id", "date"]

    def post(self, request):
        obj = FacebookSerializer(data=request.data)
        obj.is_valid()
        obj.save()
        fb_objs = Facebook.objects.all().order_by('-date')
        for i, obj in enumerate(fb_objs, start=100):
            obj.id = i
            obj.save()
        Facebook.objects.filter(id=None).delete()
        return Response(status=200)


class twitter_api(generics.ListAPIView):
    queryset = Twitter.objects.all()
    serializer_class = TwitterSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["id", "campaign_id", "date"]

    def post(self, request):
        obj = TwitterSerializer(data=request.data)
        obj.is_valid()
        obj.save()
        return Response(status=200)


def test1(request):
    return HttpResponse(
        """
        
        {"id": {"0": "1", "1": "2", "2": "k", "3": "4"},
        "title": {"0": "abc", "1": "def", "2": "ghi", "3": "jkl"},
        "likes": {"0": 3, "1": 5, "2": 3, "3": 5,
        "clicks": {"0": "10", "1": "er", "2": "6", "3": "12"}}
            
    """
    )


def test2(request):
    return HttpResponse(
        """{"id": {"0": "1", "1": "2", "2": "k", "3": "4"},
        "title": {"0": "abc", "1": "def", "2": "ghi", "3": "jkl"},
        "likes": {"0": 3, "1": 5, "2": 3, "3": 5},
        "clicks": {"0": "10", "1": "er", "2": "6", "3": "12"}}"""
    )


def test3(request):
    return HttpResponse(
        """{"id": {"0": "10", "1": "11", "2": "12"},
        "title": {"0": "jkl", "1": "mno", "2": "pqr"},
        "likes": {"0": 1, "1": 2, "2": 4},
        "clicks": {"0": "10", "1": "12", "2": "12"}}"""
    )
