from django.shortcuts import render, HttpResponse


# Create your views here.
def facebook(request):
    print(request.GET)
    return HttpResponse("Hello world")
