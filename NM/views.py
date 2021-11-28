import os
from sys import executable
from django.contrib.auth import models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from NM.models import *
from shutil import copyfile
import PyInstaller.__main__

from NM.settings import STATIC_URL

# Create views

def dashboard(request):
    if 'username' not in request.session:
        return redirect('/login')
    else:
        request.session.set_expiry(1000)
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
        result = redirect('/dashboard')
    
    else:
        result = render(request, 'login.html')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['pass']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(1000)
                request.session['username'] = username
                if username != 'shivam' and user.groups.all() is not None:
                    request.session['organisation_id'] = user.groups.all()[0].id
                result = redirect('/dashboard')
            else:
                messages.success(request, ('Incorrect User Credentials!'))
                result = redirect('/login')
    
    return result

def logout_user(request):
    logout(request)
    Session.objects.all().delete()
    return redirect('/')

def scripts(request):
    if 'username' not in request.session:
        return redirect('/login')
    else:
        request.session.set_expiry(1000)
        if request.method == 'POST':
            request.session['project_id'] = request.POST['id']
        project = Projects.objects.filter(id=request.session['project_id'])[0]
        result_scripts = Scripts.objects.filter(project_id=request.session['project_id']).select_related('device')
        projects = Projects.objects.all()
        devices = Devices.objects.all()
        return render(request, 'scripts.html', {'scripts': result_scripts, 'project_id': request.session['project_id'], 
                                                'organisation_name':request.session['organisation'], 'project':project,
                                                'projects':projects, 'devices':devices} )

def edit_script(request):
    if 'username' not in request.session:
        return redirect('/login')
    else:
        request.session.set_expiry(None)
        nm_model = request.POST['device']
        template = '404.html'
        context ={}
        if nm_model == "ISR4321":
            script = ISR4321.objects.filter(id=request.POST['script_id'])
            template = nm_model + ".html"
            context = {'script':script[0] , 'organisation_name':request.session['organisation']}
        elif nm_model == "WSC3650":
            script = WSC3650.objects.filter(id=request.POST['script_id'])
            vlans = VLAN_C3650.objects.filter(script_id=request.POST['script_id'])
            interfaces = Interface_C3650.objects.filter(script_id=request.POST['script_id'])
            acls = ACL_3650.objects.filter(script_id=request.POST['script_id'])
            aclels = []
            for acl in acls:
                aclel= ACL_EL_3650.objects.filter(acl_id=acl.id)
                aclels.append(aclel)
            users = CiscoUser.objects.filter(script_id=request.POST['script_id'])
            dhcps = DHCP_3650.objects.filter(script_id=request.POST['script_id'])
            dhcpexs = DHCP_EX_C3650.objects.filter(script_id=request.POST['script_id'])
            ospfs = OSPFv3_3650.objects.filter(script_id=request.POST['script_id'])
            stp_vlans = STP_VLAN_3650.objects.filter(script_id=request.POST['script_id'])
            template = nm_model + ".html"
            context = {'script':script[0], 'vlans':vlans, 'interfaces':interfaces, 'acls':acls, 'aclels':aclels, 'users':users, 'dhcps':dhcps, 'dhcpexs':dhcpexs, 'ospfs':ospfs, 'stp_vlans':stp_vlans, 'organisation_name':request.session['organisation']}
            print(context)
        elif nm_model == "C1000":
            script = C1000.objects.filter(id=request.POST['script_id'])
            vlans = VLAN_C1000.objects.filter(script_id=request.POST['script_id'])
            interfaces = Interface_C1000.objects.filter(script_id=request.POST['script_id'])
            acls = ACL_3650.objects.filter(script_id=request.POST['script_id'])
            aclels = []
            for acl in acls:
                aclel= ACL_EL_3650.objects.filter(acl_id=acl.id)
                aclels.append(aclel)
            users = CiscoUser.objects.filter(script_id=request.POST['script_id'])
            template = nm_model + ".html"
            context = {'script':script[0], 'vlans':vlans, 'interfaces':interfaces, 'acls':acls, 'aclels':aclels, 'users':users, 'organisation_name':request.session['organisation']}
        return render(request, template,  context)

def new_script(request):
    if 'username' not in request.session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            request.session.set_expiry(None)
            project_id = request.POST['project']
            device_id = request.POST['device']
            nm_model = Devices.objects.get(id=device_id).nm_model
            script_name = request.POST['script_name']
            script = Scripts(project_id=project_id, device_id=device_id, script_name=script_name)
            script.save()
            scripts = [script]
            return render(request, nm_model+'.html', {'data': scripts, 'organisation_name':request.session['organisation']})
  
def read_script(file, input):
    input_data = ""
    with open(file, 'r') as input_file:
        input_data = input_file.read()
    input_var = []
    input_val = []
    for k, v in input.__dict__.items():
        input_var.append('@'+str(k))
        input_val.append(str(v))      
    for i in range(len(input_var)):
        if str(input_val[i]) != "None" and input_val[i] != "":
            input_data = input_data.replace(str(input_var[i]),str(input_val[i]))
    temp_file = open('static/Temp/temp-playground.txt', 'w')  
    temp_file.write(input_data)
    temp_file.close()
    temp_file = open('static/Temp/temp-playground.txt', 'r')
    output_file = open('static/Temp/playground.txt', 'w')
    for line in temp_file:
        x = line.split('@')
        if len(x) == 1:
            output_file.writelines(line)
    output_file.close()
    output_file = open('static/Temp/playground.txt', 'r')
    output_data = output_file.read()
              
    return output_data
        
def config_producer(request):
    if request.method == 'POST':
        script_device = Devices.objects.get(id=Scripts.objects.get(id=request.POST['script_id']).device_id).nm_model
        if script_device == 'ISR4321':
            script = ISR4321.objects.filter(scripts_ptr_id=request.POST['script_id'])[0]
            file = 'static/Default_Config/ISR4321.txt'
            return read_script(file, script)
        elif script_device == "WSC3650":
            script = WSC3650.objects.filter(scripts_ptr_id=request.POST['script_id'])[0]
            input_data = read_script('static/Default_Config/WSC3650/Base.txt',script)
            
            vlans = VLAN_C3650.objects.filter(script_id=request.POST['script_id'])
            for vlan in vlans:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/VLAN_C3650.txt',vlan)    
            
            interfaces = Interface_C3650.objects.filter(script_id=request.POST['script_id'])
            for interface in interfaces:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/Interface_C3650.txt',interface)
            
            acls = ACL_3650.objects.filter(script_id=request.POST['script_id'])
            for acl in acls:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/ACL_3650.txt',acl)
                aclels = ACL_EL_3650.objects.filter(acl_id=acl.id)
                for aclel in aclels:
                    input_data += "\n" + read_script('static/Default_Config/WSC3650/ACL_EL_3650.txt',aclel)
            
            users = CiscoUser.objects.filter(script_id=request.POST['script_id'])
            for user in users:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/CiscoUser.txt',user)
                
            dhcps = DHCP_3650.objects.filter(script_id=request.POST['script_id'])
            for dhcp in dhcps:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/DHCP_3650.txt',dhcp)
                
            dhcpexs = DHCP_EX_C3650.objects.filter(script_id=request.POST['script_id'])
            for dhcpex in dhcpexs:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/DHCP_EX_C3650.txt',dhcpex)
                
            ospfs = OSPFv3_3650.objects.filter(script_id=request.POST['script_id'])
            for ospf in ospfs:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/OSPFv3_3650.txt',ospf)
                
            stp_vlans = STP_VLAN_3650.objects.filter(script_id=request.POST['script_id'])
            for stp_vlan in stp_vlans:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/STP_VLAN_3650.txt',stp_vlan)
                
            return input_data
        elif script_device == "C1000":
            script = C1000.objects.filter(scripts_ptr_id=request.POST['script_id'])[0]
            input_data = read_script('static/Default_Config/C1000/Base.txt',script)
            
            vlans = VLAN_C3650.objects.filter(script_id=request.POST['script_id'])
            for vlan in vlans:
                input_data += "\n" + read_script('static/Default_Config/C1000/VLAN_C1000.txt',vlan)    
            
            interfaces = Interface_C3650.objects.filter(script_id=request.POST['script_id'])
            for interface in interfaces:
                input_data += "\n" + read_script('static/Default_Config/C1000/Interface_C1000.txt',interface)
            
            acls = ACL_3650.objects.filter(script_id=request.POST['script_id'])
            for acl in acls:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/ACL_3650.txt',acl)
                aclels = ACL_EL_3650.objects.filter(acl_id=acl.id)
                for aclel in aclels:
                    input_data += "\n" + read_script('static/Default_Config/WSC3650/ACL_EL_3650.txt',aclel)
            
            users = CiscoUser.objects.filter(script_id=request.POST['script_id'])
            for user in users:
                input_data += "\n" + read_script('static/Default_Config/WSC3650/CiscoUser.txt',user)
                
            return input_data
    
    else:
        return redirect('/404')
    
def text_generator(request):
    
    input_data = config_producer(request)
    scriptname = Scripts.objects.filter(id=request.POST['script_id'])[0].script_name
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename='+scriptname+'.txt'
        
    response.write(input_data)
        
    return response
    
def exe_generator(request):
    
    input_data = config_producer(request)
    scriptname = Scripts.objects.filter(scripts_ptr_id=request.POST['script_id'])[0].script_name
    
    output_file = open('static/Temp/playground.txt', 'wt')
    python_output = open('static/Temp/python_playground.txt', 'wt')
    
    output_file.write(input_data)            
        
    python_output.writelines('import getpass\n')
    python_output.writelines('import sys\n')
    python_output.writelines('import telnetlib\n')
    python_output.writelines('HOST="192.168.1.1"\n')
    python_output.writelines('print("Injecting Scripts.......")\n')
    python_output.writelines('tn = telnetlib.Telnet(HOST)\n')
    python_output.writelines('tn.read_until("Router")\n')        

    output_file = open('static/Temp/playground.txt', 'r')
    
    for line in output_file:
        line = line.replace('\n', '')
        python_output.write("tn.write('"+ str(line) +"\\n')\n")
    
    python_output.writelines('tn.write("end \\n")\n')    
    python_output.writelines('tn.write("exit \\n")\n')   
    python_output = open('static/Temp/python_playground.txt', 'r')
    copyfile('static/Temp/python_playground.txt', 'static/Temp/python_playground.py')
    
    PyInstaller.__main__.run(['static/Temp/python_playground.py' ,'--onefile'])
    
    output = open('dist/python_playground.exe', 'rb')
    
    response = HttpResponse(output.read(), content_type='application/exe')
    response['Content-Disposition'] = 'attachment; filename='+scriptname+'.exe'

    return response

def save_project(request):
    if 'username' not in request.session:
        redirect('/login')
    else:
        if request.method == 'POST':
            project_name = request.POST['pname']
            client_name = request.POST['cname']
            desc = request.POST['desc']
            organisation = User.objects.get(username=request.session['username']).groups.all()
            organisation = organisation[0]
            if request.POST['id'] is not None:
                project = Projects(id=request.POST['id'],project_name=project_name, organisation=organisation, client_name=client_name, desc=desc)
                project.save()
                return redirect('/dashboard')
            else:
                project = Projects(project_name=project_name, organisation=organisation, client_name=client_name, desc=desc)
                project.save()
            request.session['project_id'] = project.id
    return redirect('/scripts')

def device_list(request):
    if 'username' not in request.session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            devices = Devices.objects.filter(device_category_id=request.POST['device']).select_related('device_category')
            return render(request, 'devices.html', {'devices': devices, 'category': devices[0].device_category.category_name, 'organisation_name':request.session['organisation']} )
    return redirect('/login')

def save(request):
    if request.method == 'POST':
        nm_model = Devices.objects.get(id=request.POST['device_id']).nm_model
        if nm_model =="ISR4321":
            script = ISR4321(
                device_id = 1,
            project_id = request.session['project_id'],
            script_name = request.POST['script_name'],
            host_name = request.POST['rname'],
            banner_motd = request.POST['motdr'],
            user_name = request.POST['uname'],
            user_pass = request.POST['spwd'],
            login_block_time = request.POST['login'],
            login_tries = request.POST['atmpt'],
            tries_time = request.POST['sec'],
            login_delay = request.POST['delay'],
            login_host = request.POST['lghost'],
            login_trap_level = request.POST['Trap'],
            login_source = request.POST['src_int'],
            en_pass_length = request.POST['en_pass_length'],
            en_pass = request.POST['enpwd'],
            domain_name = request.POST['dname'],
            isakmp_policy = request.POST['isakmp_policy'],
            isakmp_password = request.POST['iskapwd'],
            isakmp_remote_peer = request.POST['remotepeer'],
            isakmp_tag = request.POST['tag'],
            crypto_access_list = request.POST['acl'],
            crypto_permit_ip_start = request.POST['srtip'],
            crypto_permit_start_wild = request.POST['wldstrtip'],
            crypto_permit_ip_end = request.POST['endip'],
            crypto_permit_end_wild = request.POST['lstid'],
            crypto_map_name = request.POST['crypto_map_name'],
            crypto_map_num = request.POST['crypto_map_num'],
            crypto_map_match_access_list = request.POST['mcacl'],
            crypto_map_peer = request.POST['peerwan'],
            crypto_map_transform_set = request.POST['crypto_map_transform_set'],
            crypto_map_lifetime_seconds = request.POST['crypto_map_lifetime_seconds'],
            isakmp_ipv6_policy = request.POST['isakmp_ipv6_policy'],
            isakmp_ipv6_password = request.POST['cpwd'],
            isakmp_ipv6_remote_peer_ip = request.POST['isakmp_ipv6_remote_peer'],
            isakmp_ipv6_remote_peer_prefix = request.POST['prefixpeer'],
            crypto_keyring = request.POST['keyname'],
            crypto_pre_shared_key_ipv6 = request.POST['preshared'],
            crypto_pre_shared_key_prefix = request.POST['presharedpre'],
            crypto_pre_shared_key = request.POST['crypto_pre_shared_key'],
            crypto_ipsec_transform_set = request.POST['crypto_ipsec_transform_set'],
            ipsec_profile = request.POST['ipsec_profile'],
            ipsec_transform_set = request.POST['ipsec_transform_set'],
            isakmp_profile = request.POST['isakmp_profile'],
            isakmp_match_ipv6_add = request.POST['isakmpset'],
            isakmp_match_ipv6_prefix = request.POST['isakmp_match_ipv6_prefix'],
            radius_server_name = request.POST['radius_server_name'],
            server_address = request.POST['server_address'],
            max_fail = request.POST['max_fail'],
            radius_pass = request.POST['radius_pass'],
            group_name = request.POST['group_name'],
            server_name = request.POST['radius_server_name'],
            zone_name = request.POST['zone_name'],
            zone_internet = request.POST['zone_internet'],
            class_map_name = request.POST['class_map_name'],
            policy_map = request.POST['policy_map'],
            acl_name = request.POST['acl_name'],
            acl_string = request.POST['acl_string'],
            ssh_crypto_key = request.POST['ssh_crypto_key'],
            ssh_timeout = request.POST['ssh_timeout'],
            ssh_retries = request.POST['ssh_retries'],
            g00_ipv4 = request.POST['g00_ip'],
            g00_subnet = request.POST['g00_subnet'],
            g00_vrrp_num = request.POST['g00_vrrp_num'],
            g00_vrrp_address = request.POST['g00_vrrp_address'],
            g00_track_num = request.POST['g00_track_num'],
            g00_track_dec = request.POST['g00_track_dec'],
            g00_priority = request.POST['g00_priority'],
            g00_ipv6_address = request.POST['g00_ipv6_address'],
            g00_ipv6_link = request.POST['g00_ipv6_link'],
            g00_ipv6_vrrp_num = request.POST['g00_ipv6_vrrp_num'],
            g00_ipv6_vrrp_address = request.POST['g00_ipv6_vrrp_address'],
            g00_ipv6_track_num = request.POST['g00_ipv6_track_num'],
            g00_ipv6_track_dec = request.POST['g00_ipv6_track_dec'],
            g00_ipv6_priority = request.POST['g00_ipv6_priority'],
            g00_nat = request.POST['g00_nat'],
            g00_zone = request.POST['g00_zone'],
            g01_ipv4 = request.POST['g01_ip'],
            g01_subnet = request.POST['g01_subnet'],
            g01_ipv6_address = request.POST['g01_ipv6_address'],
            g01_ipv6_link = request.POST['g01_ipv6_link'],
            g01_ospfv3_ipv4 = request.POST['g01_ospfv3_ipv4'],
            g01_ospfv3_area = request.POST['g01_ospfv3_area'],
            g01_ospfv3_ipv6 = request.POST['g01_ospfv3_ipv6'],
            g01_ospfv3_v6_area = request.POST['g01_ospfv3_v6_area'],
            g01_ospfv3_encryption_num = request.POST['g01_ospfv3_encryption_num'],
            g01_ospfv3_encryption_sha = request.POST['g01_ospfv3_encryption_sha'],
            g01_nat = request.POST['g01_nat'],
            g01_zone = request.POST['g01_zone'],
            g02_ipv4 = request.POST['g02_ip'],
            g02_subnet = request.POST['g02_subnet'],
            g02_ipv6_address = request.POST['g02_ipv6_address'],
            g02_ipv6_link = request.POST['g02_ipv6_link'],
            g02_ospfv3_ipv4 = request.POST['g02_ospfv3_ipv4'],
            g02_ospfv3_area = request.POST['g02_ospfv3_area'],
            g02_ospfv3_ipv6 = request.POST['g02_ospfv3_ipv6'],
            g02_ospfv3_v6_area = request.POST['g02_ospfv3_v6_area'],
            g02_ospfv3_encryption_num = request.POST['g02_ospfv3_encryption_num'],
            g02_ospfv3_encryption_sha = request.POST['g02_ospfv3_encryption_sha'],
            g02_nat = request.POST['g02_nat'],
            g02_zone = request.POST['g02_zone'],
            lo1_ip = request.POST['lo1_ip'],
            lo1_subnet = request.POST['lo1_subnet'],
            lo1_ospfv3_ipv4 = request.POST['lo1_ospfv3_ipv4'],
            lo1_ospfv3_area = request.POST['lo1_ospfv3_area'],
            tunnel_num = request.POST['tunnel_num'],
            tunnel_ipv6_add = request.POST['tunnel_ipv6_add'],
            tunnel_ipv6_prefix = request.POST['tunnel_ipv6_prefix'],
            tunnel_source_interface = request.POST['tunnel_source_interface'],
            tunnel_destination_address = request.POST['tunnel_destination_address'],
            tunnel_protection_profile = request.POST['tunnel_protection_profile'],
            ntp_peer_add1 = request.POST['ntp_peer_add1'],
            ntp_peer_add2 = request.POST['ntp_peer_add2'],
            ntp_master_num = request.POST['ntpnum'],
            ntp_auth_key_num = request.POST['ntp_auth_key_num'],
            ntp_auth_key_pass = request.POST['ntp_auth_key_pass'],
            ntp_trust_key = request.POST['ntp_trust_key'],
            ip_prefix_list_name = request.POST['ip_prefix_list_name'],
            ip_prefix_list_network = request.POST['ip_prefix_list_network'],
            ip_prefix_list_subnet = request.POST['ip_prefix_list_subnet'],
            route_map_name = request.POST['route_map_name'],
            route_map_permit_1 = request.POST['route_map_permit_1'],
            route_map_match_list = request.POST['route_map_match_list'],
            set_weight = request.POST['set_weight'],
            set_metric = request.POST['set_metric'],
            route_map_permit_2 = request.POST['route_map_permit_2'],
            nat_pool_name = request.POST['nat_pool_name'],
            nat_start_address = request.POST['nat_start_address'],
            nat_end_address = request.POST['nat_end_address'],
            nat_subnet = request.POST['nat_subnet'],
            nat_acl_number = request.POST['nat_acl_number'],
            nat_acl_permit_ip = request.POST['nat_acl_permit_ip'],
            nat_acl_permit_wildcard = request.POST['nat_acl_permit_wildcard'],
            ospf_process_id = request.POST['ospf_process_id'],
            ospfv3_ipv4_rid = request.POST['ospfv3_ipv4_rid'],
            ospfv3_ipv6_rid = request.POST['ospfv3_ipv6_rid'],
            route_wan_lo_network = request.POST['route_wan_lo_network'],
            route_wan_lo_subnet = request.POST['route_wan_lo_subnet'],
            next_hop_wan = request.POST['next_hop_wan'],
            route_opp_lo_network = request.POST['route_opp_lo_network'],
            route_opp_lo_subnet = request.POST['route_opp_lo_subnet'],
            next_hop_router = request.POST['next_hop_router'],
            bgp_community_route_map = request.POST['neighbor_wan_lo_ip'],
            bgp_process_id = request.POST['bgp_process_id'],
            bgp_router_id = request.POST['bgp_router_id'],
            neighbor_wan_lo_ip = request.POST['neighbor_wan_lo_ip'],
            neighbor_wan_lo_as = request.POST['neighbor_wan_lo_as'],
            neighbor_wan_lo_update_ip = request.POST['neighbor_wan_lo_update_ip'],
            neighbor_wan_lo_update_int = request.POST['neighbor_wan_lo_update_int'],
            neighbor_ipv6_add = request.POST['neighbor_ipv6_add'],
            neighbor_ipv6_as = request.POST['neighbor_ipv6_as'],
            bgp_ipv4_neighbor_ip = request.POST['bgp_ipv4_neighbor_ip'],
            bgp_ipv4_network = request.POST['bgp_ipv4_network'],
            bgp_ipv4_subnet = request.POST['bgp_ipv4_subnet'],
            bgp_ipv4_neighbor_wan_ip_in = request.POST['bgp_ipv4_neighbor_wan_ip_in'],
            bgp_ipv4_neighbor_wan_route_map_in = request.POST['bgp_ipv4_neighbor_wan_route_map_in'],
            bgp_ipv4_community = request.POST['bgp_ipv4_community'],
            bgp_ipv4_neighbor_wan_ip_out = request.POST['bgp_ipv4_neighbor_wan_ip_out'],
            bgp_ipv4_neighbor_wan_route_map_out = request.POST['bgp_ipv4_neighbor_wan_route_map_out'],
            bgp_ipv6_neighbor_ip = request.POST['bgp_ipv6_neighbor_ip'],
            bgp_ipv6_network = request.POST['bgp_ipv6_network'],
            bgp_ipv6_subnet = request.POST['bgp_ipv6_subnet'],
            bgp_ipv6_neighbor_wan_ip_in = request.POST['bgp_ipv6_neighbor_wan_ip_in'],
            bgp_ipv6_neighbor_wan_route_map_in = request.POST['bgp_ipv6_neighbor_wan_route_map_in'],
            bgp_ipv6_community = request.POST['bgp_ipv6_community'],
            context=''
            )
            if 'script_id' in request.POST:
                script.scripts_ptr_id = request.POST['script_id']
            script.save()
        elif nm_model =="WSC3650":
            
            script = WSC3650(
            device_id = 2,
            script_name = request.POST['script_name'],
            project_id= request.session['project_id'],
            host_name = request.POST['host_name'],
            banner_motd = request.POST['banner_motd'],
            secret = request.POST['secret'],
            login_block_time = request.POST['login_block_time'],
            login_tries = request.POST['login_tries'],
            tries_time = request.POST['tries_time'],
            login_delay = request.POST['login_delay'],
            login_access = request.POST['login_access'],
            default_gateway = request.POST['default_gateway'],
            radius_server = request.POST['radius_server'],
            radius_ip = request.POST['radius_ip'],
            radius_key = request.POST['radius_key'],
            radius_group = request.POST['radius_group'],
            max_fail = request.POST['max_fail'],
            ntp_server = request.POST['ntp_server'],
            ntp_auth_key = request.POST['ntp_auth_key'],
            ntp_pass = request.POST['ntp_pass'],
            ntp_trust_key = request.POST['ntp_trust_key'],
            stp_mode = request.POST['stp_mode'],
            min_length = request.POST['min_length'])
            script.save()
            
            vlan = None
            interface = None
            stp = None
            dhcp = None
            dhcp_ex = None
            ospf = None
            csuser = None
            acl = None
            acl_el = None
            
            if 'script_id' in request.POST:
                script.scripts_ptr_id = request.POST['script_id']
        
            for i in range(1, int(request.POST['vlan_count'])+1):
                
                i=str(i)
                
                vlan = VLAN_C3650(
                script_id = script.scripts_ptr_id,
                number = request.POST['vlannum'+i],
                name = request.POST['vlanname'+i],
                ipv4_address = request.POST['vlanip'+i],
                ipv4_subnet = request.POST['vlansub'+i],
                ipv6_address = request.POST['vlanipv6'+i],
                ipv6_prefix = request.POST['vlanpre'+i],
                ipv6_link = request.POST['vlanlink'+i]
                )
                vlan.save()
                
                
            for i in range(1, int(request.POST['int_count'])+1):
                i=str(i)
                
                interface = Interface_C3650(
                    script_id = script.scripts_ptr_id,
                status = request.POST['intstatus'+i],
                name = request.POST['intname'+i],
                switchport = request.POST['intsw'+i],
                ipv4_address = request.POST['intip'+i],
                ipv4_subnet = request.POST['intsub'+i],
                ipv6_address = request.POST['intipv6'+i],
                ipv6_prefix = request.POST['intpre'+i],
                ipv6_link = request.POST['intlink'+i],
                sw_mode = request.POST['intswmode'+i],
                sw_access = request.POST['intswaccess'+i],
                allowed_vlan = request.POST['intallvlan'+i],
                native_vlan = request.POST['intnative'+i],
                encapsulation = request.POST['intencap'+i],
                nonegotiate = request.POST['intnoneg'+i],
                channel_group = request.POST['intch'+i],
                channel_mode = request.POST['intchmode'+i],
                stp_cost = request.POST['intstpcost'+i],
                ipv4_ospfv3 = request.POST['intipospf'+i],
                ipv4_area =request.POST['intiparea'+i],
                ipv6_ospfv3 = request.POST['intipv6ospf'+i],
                ipv6_area = request.POST['intipv6area'+i],
                )
                interface.save()
                
            for i in range(1, int(request.POST['stp_count'])+1):
                i=str(i)
                
                stp = STP_VLAN_3650(
                    script_id = script.scripts_ptr_id,
                vlan = request.POST['stpvlan'+i],
                root = request.POST['stproot'+i]
                )
                stp.save()
                
            for i in range(1, int(request.POST['dhcp_count'])+1):
                i=str(i)
                
                dhcp = DHCP_3650(
                    script_id = script.scripts_ptr_id,
                name = request.POST['dhcpname'+i],
                network_ip = request.POST['dhcpnet'+i],
                network_subnet = request.POST['dhcpsub'+i],
                default_router = request.POST['dhcprout'+i]
                )
                dhcp.save()
                
            for i in range(1, int(request.POST['ospf_count'])+1):
                i=str(i)
                
                ospf = OSPFv3_3650(
                    script_id = script.scripts_ptr_id,
                process = request.POST['ospfpro'+i],
                router_id = request.POST['ospfrid'+i]
                )
                ospf.save()
                
            for i in range(1, int(request.POST['user_count'])+1):
                i=str(i)
                
                csuser = CiscoUser(
                    script_id = script.scripts_ptr_id,
                name = request.POST['username'+i],
                password = request.POST['userpass'+i]
                )
                csuser.save()
                
            for i in range(1, int(request.POST['acl_count'])+1):
                i=str(i)
                
                acl = ACL_3650(
                    script_id = script.scripts_ptr_id,
                name = request.POST['aclname'+i]
                )
                acl.save()
                for j in range(1, int(request.POST['acl_el_count'+i])+1):
                    j=str(j)
                    ACL_EL_3650.objects.filter(acl_id = acl.id).delete()
                    acl_el = ACL_EL_3650(
                        acl_id = acl.id,
                    type = request.POST['aclcontrol'+j],
                    address = request.POST['acladd'+j]
                    )
                    acl_el.save()
                
            for i in range(1, int(request.POST['dhcp_ex_count'])+1):
                i=str(i)
                
                dhcp_ex = DHCP_EX_C3650(
                    script_id = script.scripts_ptr_id,
                    address = request.POST['dhcpex'+i]
                )
                dhcp_ex.save()
        elif nm_model =="C1000":
            
            script = C1000(
            device_id = 3,
            script_name = request.POST['script_name'],
            project_id= request.session['project_id'],
            host_name = request.POST['host_name'],
            banner_motd = request.POST['banner_motd'],
            secret = request.POST['secret'],
            login_block_time = request.POST['login_block_time'],
            login_tries = request.POST['login_tries'],
            tries_time = request.POST['tries_time'],
            login_delay = request.POST['login_delay'],
            login_access = request.POST['login_access'],
            radius_server = request.POST['radius_server'],
            radius_ip = request.POST['radius_ip'],
            radius_key = request.POST['radius_key'],
            radius_group = request.POST['radius_group'],
            max_fail = request.POST['max_fail'],
            ntp_server = request.POST['ntp_server'],
            ntp_auth_key = request.POST['ntp_auth_key'],
            ntp_pass = request.POST['ntp_pass'],
            ntp_trust_key = request.POST['ntp_trust_key'],
            stp_mode = request.POST['stp_mode'],
            min_length = request.POST['min_length'])
            script.save()
            
            vlan = None
            interface = None
            csuser = None
            acl = None
            acl_el = None
            
            if 'script_id' in request.POST:
                script.scripts_ptr_id = request.POST['script_id']
        
            for i in range(1, int(request.POST['vlan_count'])+1):
                
                i=str(i)
                
                vlan = VLAN_C1000(
                script_id = script.scripts_ptr_id,
                number = request.POST['vlannum'+i],
                name = request.POST['vlanname'+i]
                )
                vlan.save()
                
                
            for i in range(1, int(request.POST['int_count'])+1):
                i=str(i)
                
                interface = Interface_C1000(
                    script_id = script.scripts_ptr_id,
                status = request.POST['intstatus'+i],
                name = request.POST['intname'+i],
                sw_mode = request.POST['intswmode'+i],
                sw_access = request.POST['intswaccess'+i],
                allowed_vlan = request.POST['intallvlan'+i],
                native_vlan = request.POST['intnative'+i],
                channel_group = request.POST['intch'+i],
                channel_mode = request.POST['intchmode'+i],
                bdpu_filter = request.POST['bdpufilter'+i],
                bdpu_guard = request.POST['bdpuguard'+i],
                )
                interface.save()
                
              
            for i in range(1, int(request.POST['user_count'])+1):
                i=str(i)
                
                csuser = CiscoUser(
                    script_id = script.scripts_ptr_id,
                name = request.POST['username'+i],
                password = request.POST['userpass'+i]
                )
                csuser.save()
                
            for i in range(1, int(request.POST['acl_count'])+1):
                i=str(i)
                
                acl = ACL_3650(
                    script_id = script.scripts_ptr_id,
                name = request.POST['aclname'+i]
                )
                acl.save()
                for j in range(1, int(request.POST['acl_el_count'+i])+1):
                    j=str(j)
                    ACL_EL_3650.objects.filter(acl_id = acl.id).delete()
                    acl_el = ACL_EL_3650(
                        acl_id = acl.id,
                    type = request.POST['aclcontrol'+j],
                    address = request.POST['acladd'+j]
                    )
                    acl_el.save()
            
        
        
        return render(request, nm_model + '.html',  context)
        
    return redirect('/dashboard')

def profile(request):
    
    return redirect('/')
    



def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def base_router(request):
    return render(request, 'base_router.html')

def form_router(request):
    return render(request, 'form_router.html')

def base_switch(request):
    return render(request, 'C1000.html')

def base_switch3(request):
    return render(request, 'WSC3650.html')

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

def rout(request):
    return render(request, 'ISR4321.html')

def base(request):
    return render(request, 'base.html')


