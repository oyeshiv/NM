from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from NM.forms import ISR4321From
from django.contrib.auth.models import User, Group
from NM.models import ISR4321, Devices, Projects, Scripts
# Create views


def dash(request):
    
    user = User.objects.get(username=request.POST['username'])
    all_group = user.groups.all()
    user_group = 0
    organisation_name = ""
    for osn in all_group:
        user_group = osn.id
        organisation_name = osn.name.upper()
    if user_group == 2 or request.POST['username']=='shivam':
        return redirect('admin/')
    projects = Projects.objects.filter(organisation_id=user_group)
    return render(request, 'projects.html', {'projects': projects, 'user':user, 'organisation_name':organisation_name})
    


def login_user(request):

    result = render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = dash(request)
        else:
            messages.success(request, ('Incorrect User Credentials!'))
            result = render(request, 'login.html')
    return result

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

def new_script(request):
    
    return render(request, 'new_script.html')

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

def dynamic_menu(request):
    return render(request, 'dynamic_menu.html')

def index_l3(request):
    return render(request, 'index_l3.html')
def team(request):
    return render(request, 'team.html')
def team(request):
    return render(request, 'home.html')

