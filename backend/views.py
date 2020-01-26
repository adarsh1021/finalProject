from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


def hello(request):
    return render(request,"backend/index.html")


def login(request):
    return render(request, "backend/login.html")
