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

def test(request):
    return render(request, 'testing.html')

def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'home.html')
def base_router(request):
    return render(request, 'base_router.html')
def form_router(request):
    return render(request, 'form_router.html')
def base_switch(request):
    return render(request, 'base_switch.html')
def base_switch3(request):
    return render(request, 'base_switch3.html')
def form_layer3(request):
    return render(request, 'form_layer3.html')
def form_switch2(request):
    return render(request, 'form_switch2.html')
