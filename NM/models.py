from sys import _current_frames
from django.contrib.auth.models import Group
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.base import Model

class DeviceCategories(models.Model):
    category_name = models.CharField(max_length=100)

class Devices(models.Model):
    device_category = models.ForeignKey(DeviceCategories, on_delete=models.RESTRICT)
    device_model = models.CharField(max_length=100)
    device_manufacturer = models.CharField(max_length=100)
    nm_model = models.CharField(max_length=100)

    def __str__(self):
        return self.device_category.category_name + ' | ' + self.device_model

class Projects(models.Model):
    organisation = models.ForeignKey(Group, default=1, on_delete=models.RESTRICT)
    project_name = models.CharField(max_length=100)
    desc = models.TextField()
    client_name = models.CharField(max_length=100)

    def __str__(self):
        return self.project_name

class Scripts(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.RESTRICT)
    project = models.ForeignKey(Projects, on_delete=models.RESTRICT)
    date_created = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now_add=True)
    script_name = models.CharField(max_length=100)
    

class ISR4321(Scripts):
    
    host_name = models.CharField(max_length=100)
    banner_motd = models.CharField(max_length=100)
    #login security
    user_name = models.CharField(max_length=100)
    user_pass = models.CharField(max_length=100)
    login_block_time = models.IntegerField()
    login_tries = models.IntegerField()
    tries_time = models.IntegerField()
    login_delay = models.IntegerField()
    login_host = models.GenericIPAddressField()
    login_trap_level = models.CharField(max_length=100)
    login_source = models.CharField(max_length=100)
    en_pass_length = models.CharField(max_length=100)
    en_pass = models.CharField(max_length=100)
    domain_name = models.CharField(max_length=100)
    
    isakmp_policy = models.IntegerField()
    isakmp_password = models.CharField(max_length=100)
    isakmp_remote_peer = models.GenericIPAddressField()
    isakmp_tag = models.IntegerField()
    crypto_access_list = models.IntegerField()
    crypto_permit_ip_start = models.GenericIPAddressField()
    crypto_permit_start_wild = models.GenericIPAddressField()
    crypto_permit_ip_end = models.GenericIPAddressField()
    crypto_permit_end_wild = models.GenericIPAddressField()
    crypto_map_name = models.CharField(max_length=100)
    crypto_map_num = models.IntegerField()
    crypto_map_match_access_list = models.CharField(max_length=100)
    crypto_map_peer = models.GenericIPAddressField()
    crypto_map_transform_set = models.IntegerField()
    crypto_map_lifetime_seconds = models.IntegerField()

    isakmp_ipv6_policy = models.IntegerField()
    isakmp_ipv6_password = models.CharField(max_length=100)
    isakmp_ipv6_remote_peer_ip = models.GenericIPAddressField()
    isakmp_ipv6_remote_peer_prefix = models.CharField(max_length=2)
    crypto_keyring = models.CharField(max_length=100)
    crypto_pre_shared_key_ipv6 = models.GenericIPAddressField()
    crypto_pre_shared_key_prefix = models.CharField(max_length=2)
    crypto_pre_shared_key = models.CharField(max_length=100)
    crypto_ipsec_transform_set = models.CharField(max_length=100)
    
    ipsec_profile = models.CharField(max_length=100)
    ipsec_transform_set = models.CharField(max_length=100)

    isakmp_profile = models.CharField(max_length=100)
    isakmp_match_ipv6_add = models.CharField(max_length=100)
    isakmp_match_ipv6_prefix = models.CharField(max_length=2)

    #radius
    radius_server_name = models.CharField(max_length=100)
    server_address = models.GenericIPAddressField()
    max_fail = models.IntegerField()
    radius_pass = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)
    server_name = models.CharField(max_length=100)
    zone_name = models.CharField(max_length=100)
    zone_internet = models.CharField(max_length=100)
    class_map_name = models.CharField(max_length=100)
    policy_map = models.CharField(max_length=100)
    
    acl_name = models.CharField(max_length=100)
    acl_string = models.TextField()

    #ssh
    ssh_crypto_key = models.IntegerField()
    ssh_timeout = models.CharField(max_length=100)
    ssh_retries = models.CharField(max_length=100)

    #interfaces
    g00_ipv4 = models.GenericIPAddressField()
    g00_subnet = models.GenericIPAddressField()
    g00_vrrp_num = models.IntegerField()
    g00_vrrp_address = models.CharField(max_length=100)
    g00_track_num = models.IntegerField()
    g00_track_dec = models.IntegerField()
    g00_priority = models.IntegerField()
    g00_ipv6_address = models.GenericIPAddressField()
    g00_ipv6_link = models.GenericIPAddressField()
    g00_ipv6_vrrp_num = models.IntegerField()
    g00_ipv6_vrrp_address = models.CharField(max_length=100)
    g00_ipv6_track_num = models.IntegerField()
    g00_ipv6_track_dec = models.IntegerField()
    g00_ipv6_priority = models.IntegerField()
    g00_nat = models.CharField(max_length=100)
    g00_zone = models.CharField(max_length=100)
    g01_ipv4 = models.GenericIPAddressField()
    g01_subnet = models.GenericIPAddressField()
    g01_ipv6_address = models.GenericIPAddressField()
    g01_ipv6_link = models.GenericIPAddressField()
    g01_ospfv3_ipv4 = models.IntegerField()
    g01_ospfv3_area = models.IntegerField()
    g01_ospfv3_ipv6 = models.IntegerField()
    g01_ospfv3_v6_area = models.IntegerField()
    g01_ospfv3_encryption_num = models.IntegerField()
    g01_ospfv3_encryption_sha = models.PositiveBigIntegerField()
    g01_nat = models.CharField(max_length=100)
    g01_zone = models.CharField(max_length=100)

    g02_ipv4 = models.GenericIPAddressField()
    g02_subnet = models.GenericIPAddressField()

    g02_ipv6_address = models.GenericIPAddressField()
    g02_ipv6_link = models.GenericIPAddressField()
    
    g02_ospfv3_ipv4 = models.IntegerField()
    g02_ospfv3_area = models.IntegerField()
    g02_ospfv3_ipv6 = models.IntegerField()
    g02_ospfv3_v6_area = models.IntegerField()
    g02_ospfv3_encryption_num = models.IntegerField()
    g02_ospfv3_encryption_sha = models.PositiveBigIntegerField()
    
    g02_nat = models.CharField(max_length=100)
    g02_zone = models.CharField(max_length=100)

    lo1_ip = models.GenericIPAddressField()
    lo1_subnet = models.GenericIPAddressField()
    lo1_ospfv3_ipv4 = models.IntegerField()
    lo1_ospfv3_area = models.IntegerField()

    tunnel_num = models.IntegerField()
    tunnel_ipv6_add = models.GenericIPAddressField()
    tunnel_ipv6_prefix = models.CharField(max_length=2)
    tunnel_source_interface = models.CharField(max_length=100)
    tunnel_destination_address = models.CharField(max_length=100)
    tunnel_protection_profile = models.CharField(max_length=100)

    #ntp
    ntp_peer_add1 = models.GenericIPAddressField()
    ntp_peer_add2 = models.GenericIPAddressField()
    ntp_master_num = models.IntegerField()
    ntp_auth_key_num = models.IntegerField()
    ntp_auth_key_pass = models.CharField(max_length=100)
    ntp_trust_key = models.IntegerField()

    #ip_prefix
    ip_prefix_list_name = models.CharField(max_length=100)
    ip_prefix_list_network = models.GenericIPAddressField()
    ip_prefix_list_subnet = models.GenericIPAddressField()
    

    #route-map
    route_map_name = models.CharField(max_length=100)
    route_map_permit_1 = models.IntegerField()
    route_map_match_list = models.CharField(max_length=100)
    set_weight = models.IntegerField()
    set_metric = models.IntegerField()
    route_map_permit_2 = models.IntegerField()

    #nat
    nat_pool_name = models.CharField(max_length=100)
    nat_start_address = models.GenericIPAddressField()
    nat_end_address = models.GenericIPAddressField()
    nat_subnet = models.GenericIPAddressField()
    nat_acl_number = models.IntegerField()
    nat_acl_permit_ip = models.GenericIPAddressField()
    nat_acl_permit_wildcard = models.GenericIPAddressField()

    #ospfv3
    ospf_process_id = models.CharField(max_length=20)
    ospfv3_ipv4_rid = models.GenericIPAddressField()
    ospfv3_ipv6_rid = models.GenericIPAddressField()

    #ip-route
    route_wan_lo_network = models.GenericIPAddressField()
    route_wan_lo_subnet = models.GenericIPAddressField()
    next_hop_wan = models.GenericIPAddressField()
    route_opp_lo_network = models.GenericIPAddressField()
    route_opp_lo_subnet = models.GenericIPAddressField()
    next_hop_router = models.GenericIPAddressField()

    #bgp
    bgp_community_route_map = models.CharField(max_length=100)
    bgp_process_id = models.CharField(max_length=100)
    bgp_router_id = models.GenericIPAddressField()
    neighbor_wan_lo_ip = models.GenericIPAddressField()
    neighbor_wan_lo_as = models.IntegerField()
    neighbor_wan_lo_update_ip = models.GenericIPAddressField()
    neighbor_wan_lo_update_int = models.CharField(max_length=100)
    neighbor_ipv6_add = models.GenericIPAddressField()
    neighbor_ipv6_as = models.IntegerField()
    bgp_ipv4_neighbor_ip = models.GenericIPAddressField()
    bgp_ipv4_network = models.GenericIPAddressField()
    bgp_ipv4_subnet = models.GenericIPAddressField()
    bgp_ipv4_neighbor_wan_ip_in = models.GenericIPAddressField()
    bgp_ipv4_neighbor_wan_route_map_in = models.CharField(max_length=100)
    bgp_ipv4_community = models.GenericIPAddressField()
    bgp_ipv4_neighbor_wan_ip_out = models.GenericIPAddressField()
    bgp_ipv4_neighbor_wan_route_map_out = models.CharField(max_length=100)
    bgp_ipv6_neighbor_ip = models.GenericIPAddressField()
    bgp_ipv6_network = models.GenericIPAddressField()
    bgp_ipv6_subnet = models.CharField(max_length=100)
    bgp_ipv6_neighbor_wan_ip_in = models.GenericIPAddressField()
    bgp_ipv6_neighbor_wan_route_map_in = models.CharField(max_length=100)
    bgp_ipv6_community = models.GenericIPAddressField()
    
class VLAN_C3650(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    ipv4_address = models.GenericIPAddressField()
    ipv4_subnet = models.GenericIPAddressField()
    ipv6_address = models.GenericIPAddressField()
    ipv6_prefix = models.IntegerField(max_length=2)
    ipv6_link = models.GenericIPAddressField()
    
class Interface_C3650(models.Model):
    status = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    switchport = models.CharField(max_length=2)
    ipv4_address = models.GenericIPAddressField()
    ipv4_subnet = models.GenericIPAddressField()
    ipv6_address = models.GenericIPAddressField()
    ipv6_prefix = models.IntegerField(max_length=2)
    ipv6_link = models.GenericIPAddressField()
    sw_mode = models.CharField(max_length=10)
    sw_access = models.IntegerField()
    encapsulation = models.CharField(max_length=5)
    nonegotiate = models.CharField(max_length=2)
    channel_group = models.IntegerField(max_length=1)
    channel_mode = models.CharField(max_length=10)
    stp_cost = models.IntegerField(max_length=1)
    
class STP_VLAN_3650(models.Model):
    vlan = models.IntegerField()
    root = models.CharField(max_length=9)
    
class DHCP_3650(models.Model):
    name = models.CharField(max_length=100)
    network_ip = models.GenericIPAddressField()
    network_subnet = models.GenericIPAddressField()
    default_router = models.GenericIPAddressField()
    
class C1000(Scripts):
    host_name = models.CharField(max_length=100)
    
    dhcp_excluded = ArrayField()
    
    