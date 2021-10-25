from django.shortcuts import render
from django.http import HttpResponse
from NM.forms import ISR4321From

from NM.models import ISR4321, Devices, Projects, Scripts
# Create views

def dash(request):
    projects = Projects.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def scripts(request):
    result_scripts = Scripts.objects.filter(project_id=request.POST['id']).select_related('device')
    return render(request, 'scripts.html', {'scripts': result_scripts, 'project_id': request.POST['id']} )

def edit_script(request):
    
    script_device = Scripts.objects.get(id=request.POST['script_id']).device_id
    device = Devices.objects.get(id=script_device)
    template = '404.html'
    if device.device_model == 'ISR4321/K9':
        script = Scripts.objects.filter(id=request.POST['script_id']).select_related('isr4321')
        template = 'ISR4321.html'
    return render(request, template, {'data':script , 'device': device})

def form(request):

    form = ISR4321From(request.POST)

    return render(request, 'form.html', {'form':form})

def base(request):
    return render(request, 'base.html')

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
def ISR4321(request):
    return render(request, 'ISR4321.html')
def dynamic_menu(request):
    return render(request, 'dynamic_menu.html')
def index_l3(request):
    return render(request, 'index_l3.html')

