from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from NM.models import ISR4321, Devices, Projects, Scripts
import getpass, sys, telnetlib

# Create views

def dash(request):
    if 'username' not in request.session:
        return redirect('/')
    else:
        if request.session['username']=='shivam':
            return redirect('admin/')
        elif request.session['organisation_id'] == 2:
            return redirect('admin/')
        else:
            request.session['organisation'] = Group.objects.filter(id=request.session['organisation_id'])[0].name.upper()
            projects = Projects.objects.filter(organisation_id=request.session['organisation_id'])
            return render(request ,'projects.html', {'projects': projects, 'username':request.session['username'], 'organisation_name':request.session['organisation']})
    
def login_user(request):

    if 'username' in request.session:
        result = redirect('/dash')
    
    else:
        result = render(request, 'login.html')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['pass']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                logged_user = User.objects.get(username=request.session['username'])
                if username != 'shivam' and user.groups.all() is not None:
                    request.session['organisation_id'] = user.groups.all()[0].id
                result = redirect('/dash')
            else:
                messages.success(request, ('Incorrect User Credentials!'))
                result = redirect('/')
    
    return result

def logout_user(request):
    logout(request)
    Session.objects.all().delete()
    return redirect('/')

def scripts(request):
    if 'username' not in request.session:
        return redirect('/')
    else:
        if request.method == 'POST':
            request.session['project_id'] = request.POST['id']
            project = Projects.objects.filter(id=request.POST['id'])[0]
        result_scripts = Scripts.objects.filter(project_id=request.session['project_id']).select_related('device')
        return render(request, 'scripts.html', {'scripts': result_scripts, 'project_id': request.session['project_id'], 'organisation_name':request.session['organisation'], 'project':project} )

def edit_script(request):
    if 'username' not in request.session:
        return redirect('/')
    else:
        script_device = Scripts.objects.get(id=request.POST['script_id']).device_id
        device = Devices.objects.get(id=script_device)
        template = '404.html'
        if device.device_model == 'ISR4321/K9':
            script = Scripts.objects.filter(id=request.POST['script_id']).select_related('isr4321')
            template = 'ISR4321.html'
        return render(request, template, {'data':script , 'device': device} )

def new_script(request):
    if 'username' not in request.session:
        return redirect('/')
    else:
        return render(request, 'ISR4321.html', {'data': [1]})
    
def script_gen(request):
    if request.method == 'POST':
        script_device = Devices.objects.get(id=Scripts.objects.get(id=request.POST['script_id']).device_id)
        if script_device.device_model == 'ISR4321/K9':
            script = ISR4321.objects.filter(scripts_ptr_id=request.POST['script_id'])[0]
        script_var = []
        script_val = []
        with open('NM\Default_Config\ISR4321.txt', 'r') as input_file:
            input_data = input_file.read()
        output_file = open('NM/Temp/playground.txt', 'wt')
        
        for k, v in script.__dict__.items():
            script_var.append('@'+str(k))
            script_val.append(str(v))
            
        
        for i in range(len(script_var)):
            input_data = input_data.replace(str(script_var[i]),str(script_val[i]))
            
        output_data = input_data
        
        return output_data
    
    
    
    
def text_generator(request):
    
    if request.method == 'POST':
        script_device = Devices.objects.get(id=Scripts.objects.get(id=request.POST['script_id']).device_id)
        if script_device.device_model == 'ISR4321/K9':
            script = ISR4321.objects.filter(scripts_ptr_id=request.POST['script_id'])[0]
        script_var = []
        script_val = []
        with open('NM\Default_Config\ISR4321.txt', 'r') as input_file:
            input_data = input_file.read()
        output_file = open('NM/Temp/playground.txt', 'wt')
        
        for k, v in script.__dict__.items():
            script_var.append('@'+str(k))
            script_val.append(str(v))
        
        print(script_val)
        print(script_var)
            
        
        for i in range(len(script_var)):
            input_data = input_data.replace(str(script_var[i]),str(script_val[i]))
            
        output_file.write(input_data)
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename='+script.script_name+'.txt'
        
        response.write(input_data)
        
        return response
    
    else:
        return redirect('/404')
    
def exe_generator(request):
    
    if request.method == 'POST':
        script_device = Devices.objects.get(id=Scripts.objects.get(id=request.POST['script_id']).device_id)
        if script_device.device_model == 'ISR4321/K9':
            script = ISR4321.objects.filter(scripts_ptr_id=request.POST['script_id'])[0]
        script_var = []
        script_val = []
        with open('NM\Default_Config\ISR4321.txt', 'r') as input_file:
            input_data = input_file.read()
        output_file = open('NM/Temp/playground.txt', 'wt')
        python_output = open('NM/Temp/python_playground.txt', 'wt')
        
        for k, v in script.__dict__.items():
            script_var.append('@'+str(k))
            script_val.append(str(v))
        
        for i in range(len(script_var)):
            input_data = input_data.replace(str(script_var[i]),str(script_val[i]))
        
        output_file.write(input_data)            
            
        python_output.writelines('import getpass \n')
        python_output.writelines('import sys \n')
        python_output.writelines('import telnetlib \n')
        python_output.writelines('HOST="192.168.1.1" \n')
        python_output.writelines('print("Injecting Scripts.......") \n')
        python_output.writelines('tn = telnetlib.Telnet(HOST) \n')
        python_output.writelines('tn.read_until("Router") \n')        

        
        for line in output_file:    
            output_data = output_data.w("tn.write('"+ line +"\\n') \n")
        
        python_output.writelines('tn.write("end \n") \n')    
        python_output.writelines('tn.write("exit \n") \n')   
        
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename='+script.script_name+'.py'
        
        with open('NM\Temp\python_playground.txt', 'r') as input_file:
            response.write(input_file.read())
        
        return response
    
    else:
        return redirect('/404')

def new_project(request):
    if 'username' not in request.session:
        redirect('/')
    else:
        if request.method == 'POST':
            project_name = request.POST['pname']
            client_name = request.POST['cname']
            desc = request.POST['desc']
            organisation = User.objects.get(username=request.session['username']).groups.all()
            organisation = organisation[0]
            
            project = Projects(project_name=project_name, organisation=organisation, client_name=client_name, desc=desc)
            project.save()
            request.session['project_id'] = project.id
    return redirect('/scripts')

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

