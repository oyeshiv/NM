from django.shortcuts import render
from django.http import HttpResponse
from NM.forms import ScriptFrom



from NM.models import Devices, Projects, Scripts
# Create views

def index(request):
    return render(request, 'index.html')

def dash(request):
    projects = Projects.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def scripts(request):
    result_scripts = Scripts.objects.filter(project_id=request.POST['id']).select_related('device')
    return render(request, 'scripts.html', {'scripts': result_scripts})

def new_script(request):
    form = ScriptFrom(request.POST)
    return form

def base(request):
    return render(request, 'base.html')

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
