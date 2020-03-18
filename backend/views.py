from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from backend.models import Campaign, CustomTable


def hello(request):
    return render(request, "backend/index.html")


def sign_in(request):
    return render(request, "backend/sign_in.html")


@login_required(login_url="/sign_in")
def index(request):
    user = request.user
    campaigns = Campaign.objects.filter(user=user)
    customTables = CustomTable.objects.filter(user=user)
    return render(
        request,
        "backend/dashboard.html",
        {"user": user, "campaigns": campaigns, "customTables": customTables},
    )


@login_required(login_url="/sign_in")
def dataCollection(request):
    user = request.user
    return render(request, "backend/dataCollection.html", {"user": user})


@login_required(login_url="/sign_in")
def createCustomTable(request):
    user = request.user
    campaigns = Campaign.objects.filter(user=user)
    return render(
        request,
        "backend/createCustomTable.html",
        {"user": user, "campaigns": campaigns},
    )


@login_required(login_url="/sign_in")
def analytics(request, customTableId=None):
    user = request.user
    if customTableId is None:
        customTables = CustomTable.objects.filter(user=user)
        response = render(
            request, "backend/analytics.html", {"customTables": customTables}
        )
    else:
        response = render(request, "backend/analytics.html")
    return response


def sign_out(request):

    logout(request)
    return redirect("/sign_in")


def sign_up(request):

    return render(request, "backend/sign_up.html")

