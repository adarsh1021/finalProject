from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def hello(request):
    return render(request, "backend/index.html")


def sign_in(request):
    return render(request, "backend/sign_in.html")


@login_required(login_url="/sign_in")
def index(request):
    user = request.user
    return render(request, "backend/index.html", {"user": user,})


def sign_out(request):

    logout(request)
    return redirect("/sign_in")


def sign_up(request):

    return render(request, "backend/sign_up.html")

