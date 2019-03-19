from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def toto(request):
    context = {}
    return render(request,"frontend/index.html", context)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
