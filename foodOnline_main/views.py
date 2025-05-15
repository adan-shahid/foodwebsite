from django.shortcuts import HttpResponse, render

def hello(request):
    return render(request, 'home.html')