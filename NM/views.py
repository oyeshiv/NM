from django.shortcuts import render
from django.http import HttpResponse
# Create views

def home(request):
    return render(request, 'index.html')

def router_1(request):
    return render(request, 'router1.html')
    
def router_2(request):
    return render(request, 'router2.html')

def switch_1(request):
    return render(request, 'switch1.html')

def switch_2(request):
    return render(request, 'switch2.html')