from sys import executable
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from NM.models import ISR4321, Devices, Projects, Scripts
from shutil import copyfile
from distutils.core import setup
import py2exe
import urllib
import PyInstaller.__main__

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
        return render(request, template, {'data':script , 'device': device, 'organisation_name':request.session['organisation']} )

def new_script(request):
    if 'username' not in request.session:
        return redirect('/')
    else:
        return render(request, 'ISR4321.html', {'data': [1], 'organisation_name':request.session['organisation']})
    
    
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
            
        python_output.writelines('import getpass\n')
        python_output.writelines('import sys\n')
        python_output.writelines('import telnetlib\n')
        python_output.writelines('HOST="192.168.1.1"\n')
        python_output.writelines('print("Injecting Scripts.......")\n')
        python_output.writelines('tn = telnetlib.Telnet(HOST)\n')
        python_output.writelines('tn.read_until("Router")\n')        

        output_file = open('NM/Temp/playground.txt', 'r')
        
        for line in output_file:
            line = line.replace('\n', '')
            python_output.write("tn.write('"+ str(line) +"\\n')\n")
        
        python_output.writelines('tn.write("end \\n")\n')    
        python_output.writelines('tn.write("exit \\n")\n')   
        python_output = open('NM/Temp/python_playground.txt', 'r')
        copyfile('NM/Temp/python_playground.txt', 'NM/Temp/python_playground.py')
        
        PyInstaller.__main__.run(['NM/Temp/python_playground.py' ,'--onefile'])
        
        output = open('dist/python_playground.exe', 'rb')
        
        response = HttpResponse(output.read(), content_type='application/exe')
        response['Content-Disposition'] = 'attachment; filename='+script.script_name+'.exe'

        
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

def device_list(request):
    if 'username' not in request.session:
        return redirect('/')
    else:
        if request.method == 'POST':
            devices = Devices.objects.filter(device_category_id=request.POST['device']).select_related('device_category')
            return render(request, 'devices.html', {'devices': devices, 'category': devices[0].device_category.category_name, 'organisation_name':request.session['organisation']} )
    return redirect('/')

def save(request):
    if request.method == 'POST':
        device_id = request.POST['1']
        project_id = request.POST['project_id']
        script_name = "New Script"
        host_name = request.POST['rname']
        banner_motd = request.POST['motdr']
        user_name = request.POST['uname']
        user_pass = request.POST['spwd']
        login_block_time = request.POST['login']
        login_tries = request.POST['atmpt']
        tries_time = request.POST['sec']
        login_delay = request.POST['delay']
        login_host = request.POST['lghost']
        login_trap_level = request.POST['Trap']
        login_source = request.POST['src_int']
        en_pass_length = '8'
        en_pass = request.POST['enpwd']
        domain_name = request.POST['dname']
        isakmp_policy = request.POST['isakmp_policy']
        isakmp_password = request.POST['iskapwd']
        isakmp_remote_peer = request.POST['remotepeer']
        isakmp_tag = request.POST['tag']
        crypto_access_list = request.POST['acl']
        crypto_permit_ip_start = request.POST['srtip']
        crypto_permit_start_wild = request.POST['wildstrtip']
        crypto_permit_ip_end = request.POST['endip']
        crypto_permit_end_wild = request.POST['lstid']
        crypto_map_name = request.POST['crypto_map_name']
        crypto_map_num = request.POST['crypto_map_num']
        crypto_map_match_access_list = request.POST['macl']
        crypto_map_peer = request.POST['peerwan']
        crypto_map_transform_set = request.POST['crypto_map_transform_set']
        crypto_map_lifetime_seconds = request.POST['crypto_map_lifetime_seconds']
        isakmp_ipv6_policy = request.POST['isakmp_ipv6_policy']
        isakmp_ipv6_password = request.POST['cpwd']
        isakmp_ipv6_remote_peer_ip = request.POST['isakmp_ipv6_remote_peer']
        isakmp_ipv6_remote_peer_prefix = request.POST['prefixpeer']
        crypto_keyring = request.POST['keyname']
        crypto_pre_shared_key_ipv6 = request.POST['preshared']
        crypto_pre_shared_key_prefix = request.POST['presharedpre']
        crypto_pre_shared_key = request.POST['crypto_pre_shared_key']
        crypto_ipsec_transform_set = request.POST['crypto_ipsec_transform_set']
        ipsec_profile = request.POST['ipsec_profile']
        ipsec_transform_set = request.POST['ipsec_transform_set']
        isakmp_profile = request.POST['isakmp_profile']
        isakmp_match_ipv6_add = request.POST['isakmpset']
        isakmp_match_ipv6_prefix = request.POST['isakmp_match_ipv6_prefix']
        radius_server_name = request.POST['radius_server_name']
        server_address = request.POST['server_address']
        max_fail = request.POST['max_fail']
        radius_pass = request.POST['radius_pass']
        group_name = request.POST['group_name']
        server_name = request.POST['radius_server_name']
        zone_name = request.POST['zone_name']
        zone_internet = request.POST['zone_internet']
        class_map_name = request.POST['class_map_name']
        policy_map = request.POST['policy_map']
        acl_name = request.POST['acl_name']
        acl_string = request.POST['acl_string']
        ssh_crypto_key = request.POST['ssh_crypto_key']
        ssh_timeout = request.POST['ssh_timeout']
        ssh_retries = request.POST['ssh_retries']
        g00_ip = request.POST['g00_ip']
        g00_subnet = request.POST['g00_subnet']
        g00_vrrp_num = request.POST['g00_vrrp_num']
        g00_vrrp_address = request.POST['g00_vrrp_address']
        g00_track_num = request.POST['g00_track_num']
        g00_track_dec = request.POST['g00_track_dec']
        g00_priority = request.POST['g00_priority']
        g00_ipv6_address = request.POST['g00_ipv6_address']
        g00_ipv6_link = request.POST['g00_ipv6_link']
        g00_ipv6_vrrp_num = request.POST['g00_ipv6_vrrp_num']
        g00_ipv6_vrrp_address = request.POST['g00_ipv6_vrrp_address']
        g00_ipv6_track_num = request.POST['g00_ipv6_track_num']
        g00_ipv6_track_dec = request.POST['g00_ipv6_track_dec']
        g00_ipv6_priority = request.POST['g00_ipv6_priority']
        g00_nat = request.POST['g00_nat']
        g00_zone = request.POST['g00_zone']
        g01_ip = request.POST['g01_ip']
        g01_subnet = request.POST['g01_subnet']
        g01_ipv6_address = request.POST['g01_ipv6_addres']
        g01_ipv6_link = request.POST['g01_ipv6_link']
        g01_ospfv3_ipv4 = request.POST['g01_ospfv3_ipv4']
        g01_ospfv3_area = request.POST['g01_ospfv3_area']
        g01_ospfv3_ipv6 = request.POST['g01_ospfv3_ipv6']
        g01_ospfv3_v6_area = request.POST['g01_ospfv3_v6_area']
        g01_ospfv3_encryption_num = request.POST['g01_ospfv3_encryption_num']
        g01_ospfv3_encryption_sha = request.POST['g01_ospfv3_encryption_sha']
        g01_nat = request.POST['g01_nat']
        g01_zone = request.POST['g01_zone']
        g02_ip = request.POST['g02_ip']
        g02_subnet = request.POST['g02_subnet']
        g02_ipv6_address = request.POST['g02_ipv6_address']
        g02_ipv6_link = request.POST['g02_ipv6_link']
        g02_ospfv3_ipv4 = request.POST['g02_ospfv3_ipv4']
        g02_ospfv3_area = request.POST['g02_ospfv3_area']
        g02_ospfv3_ipv6 = request.POST['g02_ospfv3_ipv6']
        g02_ospfv3_v6_area = request.POST['g02_ospfv3_v6_area']
        g02_ospfv3_encryption_num = request.POST['g02_ospfv3_encryption_num']
        g02_ospfv3_encryption_sha = request.POST['g02_ospfv3_encryption_sha']
        g02_nat = request.POST['g02_nat ']
        g02_zone = request.POST['g02_zone']
        lo1_ip = request.POST['lo1_ip']
        lo1_subnet = request.POST['lo1_subnet']
        lo1_ospfv3_ipv4 = request.POST['lo1_ospfv3_ipv4']
        lo1_ospfv3_area = request.POST['lo1_ospfv3_area']
        tunnel_num = request.POST['tunnel_num']
        tunnel_ipv6_add = request.POST['tunnel_ipv6_add']
        tunnel_ipv6_prefix = request.POST['tunnel_ipv6_prefix']
        tunnel_source_interface = request.POST['tunnel_source_interface']
        tunnel_destination_address = request.POST['tunnel_destination_address']
        tunnel_protection_profile = request.POST['tunnel_protection_profile']
        ntp_peer_add1 = request.POST['ntp_peer_add1']
        ntp_peer_add2 = request.POST['ntp_peer_add2']
        ntp_master_num = request.POST['ntpnum']
        ntp_auth_key_num = request.POST['ntp_auth_key_num']
        ntp_auth_key_pass = request.POST['ntp_auth_key_pass']
        ntp_trust_key = request.POST['ntp_trust_key']
        ip_prefix_list_name = request.POST['ip_prefix_list_name']
        ip_prefix_list_network = request.POST['ip_prefix_list_network']
        ip_prefix_list_subnet = request.POST['ip_prefix_list_subnet']
        route_map_name = request.POST['route_map_name']
        route_map_permit_1 = request.POST['route_map_permit_1']
        route_map_match_list = request.POST['route_map_match_list']
        set_weight = request.POST['set_weight']
        set_metric = request.POST['set_metric']
        route_map_permit_2 = request.POST['route_map_permit_2']
        nat_pool_name = request.POST['nat_pool_name']
        nat_start_address = request.POST['nat_start_address']
        nat_end_address = request.POST['nat_end_address']
        nat_subnet = request.POST['nat_subnet']
        nat_acl_number = request.POST['nat_acl_number']
        nat_acl_permit_ip = request.POST['nat_acl_permit_ip']
        nat_acl_permit_wildcard = request.POST['nat_acl_permit_wildcard']
        ospf_process_id = request.POST['ospf_process_id']
        ospfv3_ipv4_rid = request.POST['ospfv3_ipv4_rid']
        ospfv3_ipv6_rid = request.POST['ospfv3_ipv6_rid']
        route_wan_lo_network = request.POST['route_wan_lo_network']
        route_wan_lo_subnet = request.POST['route_wan_lo_subnet']
        next_hop_wan = request.POST['next_hop_wan']
        route_opp_lo_network = request.POST['route_opp_lo_network']
        route_opp_lo_subnet = request.POST['route_opp_lo_subnet']
        next_hop_router = request.POST['next_hop_router']
        
        
        bgp_community_route_map = request.POST['neighbor_wan_lo_ip']
        bgp_process_id = request.POST['bgp_process_id']
        bgp_router_id = request.POST['bgp_router_id']
        neighbor_wan_lo_ip = request.POST['neighbor_wan_lo_ip']
        neighbor_wan_lo_as = request.POST['neighbor_wan_lo_as']
        neighbor_wan_lo_update_ip = request.POST['neighbor_wan_lo_ip']
        neighbor_wan_lo_update_int = 'g0/0'
        neighbor_ipv6_add = request.POST['bgp_ipv4_neighbor_wan_ip_in']
        neighbor_ipv6_as = request.POST['neighbor_wan_lo_as']
        bgp_ipv4_neighbor_ip = request.POST['neighbor_wan_lo_ip']
        bgp_ipv4_network = request.POST['bgp_ipv4_network']
        bgp_ipv4_subnet = request.POST['bgp_ipv4_subnet']
        bgp_ipv4_neighbor_wan_ip_in = request.POST['bgp_ipv4_neighbor_wan_ip_in']
        bgp_ipv4_neighbor_wan_route_map_in = request.POST['neighbor_wan_lo_as']
        bgp_ipv4_community = request.POST['neighbor_wan_lo_ip']
        bgp_ipv4_neighbor_wan_ip_out = request.POST['neighbor_wan_lo_ip']
        bgp_ipv4_neighbor_wan_route_map_out = request.POST['neighbor_wan_lo_as']
        bgp_ipv6_neighbor_ip = request.POST['bgp_ipv6_neighbor_ip']
        bgp_ipv6_network = request.POST['bgp_ipv6_network']
        bgp_ipv6_subnet = request.POST['bgp_ipv6_subnet']
        bgp_ipv6_neighbor_wan_ip_in = request.POST['bgp_ipv4_neighbor_wan_ip_in']
        bgp_ipv6_neighbor_wan_route_map_in = request.POST['neighbor_wan_lo_as']
        bgp_ipv6_community = request.POST['bgp_ipv6_neighbor_ip']
        
        script = ISR4321(device_id, project_id, script_name, host_name, banner_motd, user_name, user_pass, login_block_time, login_tries, tries_time, login_delay, login_host, login_trap_level, login_source, en_pass_length, en_pass, domain_name, isakmp_policy, isakmp_password, isakmp_remote_peer, isakmp_tag, crypto_access_list, crypto_permit_ip_start, crypto_permit_start_wild, crypto_permit_ip_end, crypto_permit_end_wild, crypto_map_name, crypto_map_num, crypto_map_match_access_list, crypto_map_peer, crypto_map_transform_set, crypto_map_lifetime_seconds, isakmp_ipv6_policy, isakmp_ipv6_password, isakmp_ipv6_remote_peer_ip, isakmp_ipv6_remote_peer_prefix, crypto_keyring, crypto_pre_shared_key_ipv6, crypto_pre_shared_key_prefix, crypto_pre_shared_key, crypto_ipsec_transform_set, ipsec_profile, ipsec_transform_set, isakmp_profile, isakmp_match_ipv6_add, isakmp_match_ipv6_prefix, radius_server_name, server_address, max_fail, radius_pass, group_name, server_name, zone_name, zone_internet, class_map_name, policy_map, acl_name, acl_string, ssh_crypto_key, ssh_timeout, ssh_retries, g00_ip, g00_subnet, g00_vrrp_num, g00_vrrp_address, g00_track_num, g00_track_dec, g00_priority, g00_ipv6_address, g00_ipv6_link, g00_ipv6_vrrp_num, g00_ipv6_vrrp_address, g00_ipv6_track_num, g00_ipv6_track_dec, g00_ipv6_priority, g00_nat, g00_zone, g01_ip, g01_subnet, g01_ipv6_address, g01_ipv6_link, g01_ospfv3_ipv4, g01_ospfv3_area, g01_ospfv3_ipv6, g01_ospfv3_v6_area, g01_ospfv3_encryption_num, g01_ospfv3_encryption_sha, g01_nat, g01_zone, g02_ip, g02_subnet, g02_ipv6_address, g02_ipv6_link, g02_ospfv3_ipv4, g02_ospfv3_area, g02_ospfv3_ipv6, g02_ospfv3_v6_area, g02_ospfv3_encryption_num, g02_ospfv3_encryption_sha, g02_nat, g02_zone, lo1_ip, lo1_subnet, lo1_ospfv3_ipv4, lo1_ospfv3_area, tunnel_num, tunnel_ipv6_add, tunnel_ipv6_prefix, tunnel_source_interface, tunnel_destination_address, tunnel_protection_profile, ntp_peer_add1, ntp_peer_add2, ntp_master_num, ntp_auth_key_num, ntp_auth_key_pass, ntp_trust_key, ip_prefix_list_name, ip_prefix_list_network, ip_prefix_list_subnet, route_map_name, route_map_permit_1, route_map_match_list, set_weight, set_metric, route_map_permit_2, nat_pool_name, nat_start_address, nat_end_address, nat_subnet, nat_acl_number, nat_acl_permit_ip, nat_acl_permit_wildcard, ospf_process_id, ospfv3_ipv4_rid, ospfv3_ipv6_rid, route_wan_lo_network, route_wan_lo_subnet, next_hop_wan, route_opp_lo_network, route_opp_lo_subnet, next_hop_router, bgp_community_route_map, bgp_process_id, bgp_router_id, neighbor_wan_lo_ip, neighbor_wan_lo_as, neighbor_wan_lo_update_ip, neighbor_wan_lo_update_int, neighbor_ipv6_add, neighbor_ipv6_as, bgp_ipv4_neighbor_ip, bgp_ipv4_network, bgp_ipv4_subnet, bgp_ipv4_neighbor_wan_ip_in, bgp_ipv4_neighbor_wan_route_map_in, bgp_ipv4_community, bgp_ipv4_neighbor_wan_ip_out, bgp_ipv4_neighbor_wan_route_map_out, bgp_ipv6_neighbor_ip, bgp_ipv6_network, bgp_ipv6_subnet, bgp_ipv6_neighbor_wan_ip_in, bgp_ipv6_neighbor_wan_route_map_in, bgp_ipv6_community)
        
        script.save()
        
        return redirect('dash')
        
    return redirect('/')

def profile(request):
    
    return redirect('/')
    

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

