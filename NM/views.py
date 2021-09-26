from django.shortcuts import render
from django.http import HttpResponse
# Create views

def home(request):
    return render(request, 'index.html')