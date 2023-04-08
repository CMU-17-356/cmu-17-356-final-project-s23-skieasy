from django.http import HttpResponse
from django.shortcuts import render


def homePageView(request):
    return HttpResponse("<body><h1>Hello From SkiEasy!</h1></body>")
