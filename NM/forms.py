from django.forms import ModelForm
from NM.models import ISR4321, Scripts
from django.views.generic import CreateView

class New_Script(CreateView):
    model = ISR4321
    template_name = 'new_script.html'
    fields = '__all__'

class ISR4321From(ModelForm):

    class Meta:
        model = ISR4321
        fields = [
    'user_name', 
    'user_pass', 
    'login_block_time', 
    'login_tries', 
    'login_tries_time', 
    'login_delay', 
    'login_host', 
    'login_trap_level', 
    'en_pass_length', 
    'en_pass', 
    'domain_name', 


    'keychain_name', 
    'key_string', 
    'algo', 
    'isakmp_policy', 
    'isakmp_password', 
    'isakmp_remote_peer', 
    'isakmp_tag', 
    'crypto_access_list', 
    'crypto_permit_ip_address', 
    'crypto_map_name', 
    'crypto_map_num', 
    'crypto_map_match_access_list', 
    'crypto_map_peer', 
    'crypto_map_transform_set', 
    'crypto_map_lifetime_seconds', 

    'isakmp_ipv6_policy', 
    'isakmp_ipv6_password', 
    'isakmp_ipv6_remote_peer', 
    'crypto_keyring', 
    'crypto_pre_shared_key_ipv6', 
    'crypto_pre_shared_key', 
    'crypto_ipsec_transform_set', 
    
    'ipsec_profile', 
    'ipsec_transform_set', 

    'isakmp_profile', 
    'isakmp_match_ipv6', 


    'radius_server_name', 
    'server_address', 
    'radius_pass', 
    'group_name', 
    'server_name', 
    'zone_name', 
    'class_map_name', 
    'match_tcp', 
    'match_udp', 
    'match_icmp', 
    'match_https', 
    'match_ssh', 
    'policy_map', 
    'inspect', 
    'acl_name', 
    'acl_string', 


    'enable', 
    'ssh_timeout', 
    'ssh_retries', 

    'g00_ip', 
    'g00_subnet', 
    'g00_vrrp_num', 
    'g00_vrrp_address', 
    'g00_track_num', 
    'g00_track_dec', 
    'g00_priority', 
    'g00_ipv6', 
    'g00_ipv6_address', 
    'g00_ipv6_link', 
    'g00_ipv6_vrrp_num', 
    'g00_ipv6_vrrp_address', 
    'g00_ipv6_track_num', 
    'g00_ipv6_track_dec', 
    'g00_ipv6_priority', 
    'g00_ospfv3_ipv4', 
    'g00_ospfv3_area', 
    'g00_ospfv3_ipv6', 
    'g00_ospfv3_ipv6_area', 
    'g00_ospfv3_encryption_num', 
    'g00_ospfv3_encryption_sha', 
    'g00_zone', 

    'g01_ip', 
    'g01_subnet', 
    'g01_vrrp_num', 
    'g01_vrrp_address', 
    'g01_track_num', 
    'g01_track_dec', 
    'g01_priority', 
    'g01_ipv6', 
    'g01_ipv6_address', 
    'g01_ipv6_link', 
    'g01_ipv6_vrrp_num', 
    'g01_ipv6_vrrp_address', 
    'g01_ipv6_track_num', 
    'g01_ipv6_track_dec', 
    'g01_ipv6_priority', 
    'g01_ospfv3_ipv4', 
    'g01_ospfv3_area', 
    'g01_ospfv3_ipv6', 
    'g01_ospfv3_ipv6_area', 
    'g01_ospfv3_encryption_num', 
    'g01_ospfv3_encryption_sha', 
    'g01_zone', 

    'g02_ip', 
    'g02_subnet', 
    'g02_vrrp_num', 
    'g02_vrrp_address', 
    'g02_track_num', 
    'g02_track_dec', 
    'g02_priority', 
    'g02_ipv6', 
    'g02_ipv6_address', 
    'g02_ipv6_link', 
    'g02_ipv6_vrrp_num', 
    'g02_ipv6_vrrp_address', 
    'g02_ipv6_track_num', 
    'g02_ipv6_track_dec', 
    'g02_ipv6_priority', 
    'g02_ospfv3_ipv4', 
    'g02_ospfv3_area', 
    'g02_ospfv3_ipv6', 
    'g02_ospfv3_ipv6_area', 
    'g02_ospfv3_encryption_num', 
    'g02_ospfv3_encryption_sha', 
    'g02_zone', 

    'lo1_ip', 
    'lo1_subnet', 
    'lo1_ipv6', 
    'lo1_ospfv3_ipv4', 
    'lo1_ospfv3_area', 

    'tunnel_num', 
    'tunnel_ipv6_add', 
    'tunnel_ipv6', 
    'tunnel_source_interface', 

    'ntp_peer_add', 
    'ntp_master_num', 
    'ntp_auth_key_num', 
    'ntp_auth_key_pass', 

    'ip_prefix_list_name', 
    'ip_prefix_list_network', 

    'route_map_name', 
    'route_map_permit_1', 
    'route_map_match_list', 
    'set_weight', 
    'set_metric', 
    'route_map_permit_2', 


    'nat_pool_name', 
    'nat_start_address', 
    'nat_end_address', 
    'nat_inside_list', 

    'ospf_process_id', 
    'ospfv3_ipv4_rid', 
    'ospfv3_ipv6_rid', 


    'route_wan_lo_network', 
    'route_wan_lo_subnet', 
    'route_opp_lo_network', 
    'route_opp_lo_subnet', 


    'bgp_community_route_map', 
    'bgp_process_id', 
    'bgp_router_id', 
    'neighbor_wan_lo_ip', 
    'neighbor_wan_lo_as', 
    'neighbor_wan_lo_update_ip', 
    'neighbor_wan_lo_update_int', 
    'neighbor_ipv6_add', 
    'neighbor_ipv6_as', 
    'bgp_ipv4_neighbor_ip', 
    'bgp_ipv4_network', 
    'bgp_ipv4_subnet', 
    'bgp_ipv4_neighbor_wan_ip_in', 
    'bgp_ipv4_neighbor_wan_route_map_in', 
    'bgp_ipv4_neighbor_wan_ip_out', 
    'bgp_ipv4_neighbor_wan_route_map_out', 
    'bgp_ipv6_neighbor_ip', 
    'bgp_ipv6_network', 
    'bgp_ipv6_subnet', 
    'bgp_ipv6_neighbor_wan_ip_in', 
    'bgp_ipv6_neighbor_wan_route_map_in', 
    'bgp_ipv6_neighbor_wan_ip_out', 
    'bgp_ipv6_neighbor_wan_route_map_out' ]
