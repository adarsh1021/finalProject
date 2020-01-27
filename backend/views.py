from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User


def hello(request):
    return render(request,"backend/index.html")


def sign_in(request):
    return render(request, "backend/sign_in.html")


def index(request):
    return render(request, 'backend/index.html')


def sign_out(request):

    try:
        del request.session['user']
    except KeyError:
        pass

    return redirect('/sign_in')

def sign_up(request):

    return render(request, 'backend/sign_up.html')