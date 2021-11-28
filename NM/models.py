from sys import _current_frames
from django.contrib.auth.models import Group
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import *
import django.utils.timezone

class DeviceCategories(Model):
    category_name = CharField(max_length=100)
    
    def __str__(self):
        return self.category_name

class Devices(Model):
    device_category = ForeignKey(DeviceCategories, on_delete=RESTRICT)
    device_model = CharField(max_length=100)
    device_manufacturer = CharField(max_length=100)
    nm_model = CharField(max_length=100)

    def __str__(self):
        return self.device_category.category_name + ' | ' + self.device_model

class Projects(Model):
    organisation = ForeignKey(Group, default=1, on_delete=RESTRICT)
    project_name = CharField(max_length=100)
    desc = TextField()
    client_name = CharField(max_length=100)

    def __str__(self):
        return self.project_name

class Scripts(Model):
    device = ForeignKey(Devices, on_delete=RESTRICT)
    project = ForeignKey(Projects, on_delete=RESTRICT)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(default=django.utils.timezone.now)
    script_name = CharField(max_length=100)
    
    def __str__(self):
        return self.script_name + " | " + str(self.date_created)

class ISR4321(Scripts):
    
    host_name = CharField(max_length=100)
    banner_motd = CharField(max_length=100)
    #login security
    user_name = CharField(max_length=100)
    user_pass = CharField(max_length=100)
    login_block_time = IntegerField()
    login_tries = IntegerField()
    tries_time = IntegerField()
    login_delay = IntegerField()
    login_host = GenericIPAddressField()
    login_trap_level = CharField(max_length=100)
    login_source = CharField(max_length=100)
    en_pass_length = CharField(max_length=100)
    en_pass = CharField(max_length=100)
    domain_name = CharField(max_length=100)
    
    isakmp_policy = IntegerField()
    isakmp_password = CharField(max_length=100)
    isakmp_remote_peer = GenericIPAddressField()
    isakmp_tag = IntegerField()
    crypto_access_list = IntegerField()
    crypto_permit_ip_start = GenericIPAddressField()
    crypto_permit_start_wild = GenericIPAddressField()
    crypto_permit_ip_end = GenericIPAddressField()
    crypto_permit_end_wild = GenericIPAddressField()
    crypto_map_name = CharField(max_length=100)
    crypto_map_num = IntegerField()
    crypto_map_match_access_list = CharField(max_length=100)
    crypto_map_peer = GenericIPAddressField()
    crypto_map_transform_set = IntegerField()
    crypto_map_lifetime_seconds = IntegerField()

    isakmp_ipv6_policy = IntegerField()
    isakmp_ipv6_password = CharField(max_length=100)
    isakmp_ipv6_remote_peer_ip = GenericIPAddressField()
    isakmp_ipv6_remote_peer_prefix = CharField(max_length=2)
    crypto_keyring = CharField(max_length=100)
    crypto_pre_shared_key_ipv6 = GenericIPAddressField()
    crypto_pre_shared_key_prefix = CharField(max_length=2)
    crypto_pre_shared_key = CharField(max_length=100)
    crypto_ipsec_transform_set = CharField(max_length=100)
    
    ipsec_profile = CharField(max_length=100)
    ipsec_transform_set = CharField(max_length=100)

    isakmp_profile = CharField(max_length=100)
    isakmp_match_ipv6_add = CharField(max_length=100)
    isakmp_match_ipv6_prefix = CharField(max_length=2)

    #radius
    radius_server_name = CharField(max_length=100)
    server_address = GenericIPAddressField()
    max_fail = IntegerField()
    radius_pass = CharField(max_length=100)
    group_name = CharField(max_length=100)
    server_name = CharField(max_length=100)
    zone_name = CharField(max_length=100)
    zone_internet = CharField(max_length=100)
    class_map_name = CharField(max_length=100)
    policy_map = CharField(max_length=100)
    
    acl_name = CharField(max_length=100)
    acl_string = TextField()

    #ssh
    ssh_crypto_key = IntegerField()
    ssh_timeout = CharField(max_length=100)
    ssh_retries = CharField(max_length=100)

    #interfaces
    g00_ipv4 = GenericIPAddressField()
    g00_subnet = GenericIPAddressField()
    g00_vrrp_num = IntegerField()
    g00_vrrp_address = CharField(max_length=100)
    g00_track_num = IntegerField()
    g00_track_dec = IntegerField()
    g00_priority = IntegerField()
    g00_ipv6_address = GenericIPAddressField()
    g00_ipv6_link = GenericIPAddressField()
    g00_ipv6_vrrp_num = IntegerField()
    g00_ipv6_vrrp_address = CharField(max_length=100)
    g00_ipv6_track_num = IntegerField()
    g00_ipv6_track_dec = IntegerField()
    g00_ipv6_priority = IntegerField()
    g00_nat = CharField(max_length=100)
    g00_zone = CharField(max_length=100)
    g01_ipv4 = GenericIPAddressField()
    g01_subnet = GenericIPAddressField()
    g01_ipv6_address = GenericIPAddressField()
    g01_ipv6_link = GenericIPAddressField()
    g01_ospfv3_ipv4 = IntegerField()
    g01_ospfv3_area = IntegerField()
    g01_ospfv3_ipv6 = IntegerField()
    g01_ospfv3_v6_area = IntegerField()
    g01_ospfv3_encryption_num = IntegerField()
    g01_ospfv3_encryption_sha = PositiveBigIntegerField()
    g01_nat = CharField(max_length=100)
    g01_zone = CharField(max_length=100)

    g02_ipv4 = GenericIPAddressField()
    g02_subnet = GenericIPAddressField()

    g02_ipv6_address = GenericIPAddressField()
    g02_ipv6_link = GenericIPAddressField()
    
    g02_ospfv3_ipv4 = IntegerField()
    g02_ospfv3_area = IntegerField()
    g02_ospfv3_ipv6 = IntegerField()
    g02_ospfv3_v6_area = IntegerField()
    g02_ospfv3_encryption_num = IntegerField()
    g02_ospfv3_encryption_sha = PositiveBigIntegerField()
    
    g02_nat = CharField(max_length=100)
    g02_zone = CharField(max_length=100)

    lo1_ip = GenericIPAddressField()
    lo1_subnet = GenericIPAddressField()
    lo1_ospfv3_ipv4 = IntegerField()
    lo1_ospfv3_area = IntegerField()

    tunnel_num = IntegerField()
    tunnel_ipv6_add = GenericIPAddressField()
    tunnel_ipv6_prefix = CharField(max_length=2)
    tunnel_source_interface = CharField(max_length=100)
    tunnel_destination_address = CharField(max_length=100)
    tunnel_protection_profile = CharField(max_length=100)

    #ntp
    ntp_peer_add1 = GenericIPAddressField()
    ntp_peer_add2 = GenericIPAddressField()
    ntp_master_num = IntegerField()
    ntp_auth_key_num = IntegerField()
    ntp_auth_key_pass = CharField(max_length=100)
    ntp_trust_key = IntegerField()

    #ip_prefix
    ip_prefix_list_name = CharField(max_length=100)
    ip_prefix_list_network = GenericIPAddressField()
    ip_prefix_list_subnet = GenericIPAddressField()
    

    #route-map
    route_map_name = CharField(max_length=100)
    route_map_permit_1 = IntegerField()
    route_map_match_list = CharField(max_length=100)
    set_weight = IntegerField()
    set_metric = IntegerField()
    route_map_permit_2 = IntegerField()

    #nat
    nat_pool_name = CharField(max_length=100)
    nat_start_address = GenericIPAddressField()
    nat_end_address = GenericIPAddressField()
    nat_subnet = GenericIPAddressField()
    nat_acl_number = IntegerField()
    nat_acl_permit_ip = GenericIPAddressField()
    nat_acl_permit_wildcard = GenericIPAddressField()

    #ospfv3
    ospf_process_id = CharField(max_length=20)
    ospfv3_ipv4_rid = GenericIPAddressField()
    ospfv3_ipv6_rid = GenericIPAddressField()

    #ip-route
    route_wan_lo_network = GenericIPAddressField()
    route_wan_lo_subnet = GenericIPAddressField()
    next_hop_wan = GenericIPAddressField()
    route_opp_lo_network = GenericIPAddressField()
    route_opp_lo_subnet = GenericIPAddressField()
    next_hop_router = GenericIPAddressField()

    #bgp
    bgp_community_route_map = CharField(max_length=100)
    bgp_process_id = CharField(max_length=100)
    bgp_router_id = GenericIPAddressField()
    neighbor_wan_lo_ip = GenericIPAddressField()
    neighbor_wan_lo_as = IntegerField()
    neighbor_wan_lo_update_ip = GenericIPAddressField()
    neighbor_wan_lo_update_int = CharField(max_length=100)
    neighbor_ipv6_add = GenericIPAddressField()
    neighbor_ipv6_as = IntegerField()
    bgp_ipv4_neighbor_ip = GenericIPAddressField()
    bgp_ipv4_network = GenericIPAddressField()
    bgp_ipv4_subnet = GenericIPAddressField()
    bgp_ipv4_neighbor_wan_ip_in = GenericIPAddressField()
    bgp_ipv4_neighbor_wan_route_map_in = CharField(max_length=100)
    bgp_ipv4_community = GenericIPAddressField()
    bgp_ipv4_neighbor_wan_ip_out = GenericIPAddressField()
    bgp_ipv4_neighbor_wan_route_map_out = CharField(max_length=100)
    bgp_ipv6_neighbor_ip = GenericIPAddressField()
    bgp_ipv6_network = GenericIPAddressField()
    bgp_ipv6_subnet = CharField(max_length=100)
    bgp_ipv6_neighbor_wan_ip_in = GenericIPAddressField()
    bgp_ipv6_neighbor_wan_route_map_in = CharField(max_length=100)
    bgp_ipv6_community = GenericIPAddressField()
          
class WSC3650(Scripts):
    host_name = CharField(max_length=100)
    banner_motd = CharField(max_length=100)
    min_length = IntegerField()
    secret = CharField(max_length=100)
    
    login_block_time = IntegerField()
    login_tries = IntegerField()
    tries_time = IntegerField()
    login_delay = IntegerField()
    login_access = CharField(max_length=100)
    
    stp_mode = CharField(max_length=100)
    
    default_gateway = GenericIPAddressField()
    
    radius_server = CharField(max_length=100)
    radius_group = CharField(max_length=100)
    radius_ip = GenericIPAddressField()
    radius_key = CharField(max_length=100)
    max_fail = IntegerField()
    
    ntp_server = GenericIPAddressField()
    ntp_auth_key = IntegerField()
    ntp_pass = CharField(max_length=100)
    ntp_trust_key = IntegerField()
    
class DHCP_EX_C3650(models.Model):
    script = ForeignKey(WSC3650, on_delete=CASCADE)
    address = GenericIPAddressField()
    
class VLAN_C3650(Model):
    script = ForeignKey(WSC3650, on_delete=CASCADE)
    number = IntegerField()
    name = CharField(max_length=100, null = True)
    ipv4_address = GenericIPAddressField(null = True)
    ipv4_subnet = GenericIPAddressField(null = True)
    ipv6_address = GenericIPAddressField(null = True)
    ipv6_prefix = IntegerField(null = True)
    ipv6_link = GenericIPAddressField(null = True)
    
class Interface_C3650(Model):
    script = ForeignKey(WSC3650, on_delete=CASCADE)
    status = CharField(max_length=8, null = True)
    name = CharField(max_length=100)
    switchport = CharField(max_length=10, null = True)
    ipv4_address = GenericIPAddressField(null = True)
    ipv4_subnet = GenericIPAddressField(null = True)
    ipv6_address = GenericIPAddressField(null = True)
    ipv6_prefix = CharField(max_length=10,null = True)
    ipv6_link = GenericIPAddressField(null = True)
    sw_mode = CharField(max_length=10,null = True)
    sw_access = CharField(max_length=100,null = True)
    allowed_vlan = CharField(max_length=100,null = True)
    native_vlan = CharField(max_length=100,null = True)
    encapsulation = CharField(max_length=5,null = True)
    nonegotiate = CharField(max_length=11, null = True)
    channel_group = CharField(max_length=100,null = True)
    channel_mode = CharField(max_length=10, null = True)
    stp_cost = CharField(max_length=100,null = True)
    ipv4_ospfv3 = CharField(max_length=10,null = True)
    ipv4_area =CharField(max_length=10,null = True)
    ipv6_ospfv3 = CharField(max_length=10,null = True)
    ipv6_area = CharField(max_length=10,null = True)
    
class STP_VLAN_3650(Model):
    script = ForeignKey(WSC3650, on_delete=CASCADE)
    vlan = IntegerField()
    root = CharField(max_length=9)
    
class DHCP_3650(Model):
    script = ForeignKey(WSC3650, on_delete=CASCADE)
    name = CharField(max_length=100)
    network_ip = GenericIPAddressField()
    network_subnet = GenericIPAddressField()
    default_router = GenericIPAddressField()
    
class OSPFv3_3650(Model):
    script = ForeignKey(WSC3650, on_delete=CASCADE)
    process = CharField(max_length=10)
    router_id = GenericIPAddressField()
    
class CiscoUser(Model):
    script = ForeignKey(Scripts, on_delete=CASCADE)
    name = CharField(max_length=100)
    password = CharField(max_length=100)
    
class ACL_3650(Model):
    script = ForeignKey(Scripts, on_delete=CASCADE)
    name = CharField(max_length=100)
    
class ACL_EL_3650(Model):
    acl = ForeignKey(ACL_3650, on_delete=CASCADE)
    type = CharField(max_length=10)
    address = GenericIPAddressField()
    
class C1000(Scripts):
    host_name = CharField(max_length=100)
    banner_motd = CharField(max_length=100)
    min_length = IntegerField()
    secret = CharField(max_length=100)
    
    login_block_time = IntegerField()
    login_tries = IntegerField()
    tries_time = IntegerField()
    login_delay = IntegerField()
    login_access = CharField(max_length=100)
    
    stp_mode = CharField(max_length=100)
    
    radius_server = CharField(max_length=100)
    radius_group = CharField(max_length=100)
    radius_ip = GenericIPAddressField()
    radius_key = CharField(max_length=100)
    max_fail = IntegerField()
    
    ntp_server = GenericIPAddressField()
    ntp_auth_key = IntegerField()
    ntp_pass = CharField(max_length=100)
    ntp_trust_key = IntegerField()
    
class VLAN_C1000(Model):
    script = ForeignKey(C1000, on_delete=CASCADE)
    number = IntegerField()
    name = CharField(max_length=100, null = True)
    
class Interface_C1000(Model):
    script = ForeignKey(C1000, on_delete=CASCADE)
    status = CharField(max_length=8, null = True)
    name = CharField(max_length=100)
    sw_mode = CharField(max_length=10,null = True)
    sw_access = CharField(max_length=100,null = True)
    allowed_vlan = CharField(max_length=100,null = True)
    native_vlan = CharField(max_length=100,null = True)
    channel_group = CharField(max_length=100,null = True)
    channel_mode = CharField(max_length=10, null = True)
    bdpu_filter = CharField(max_length=10, null=True)
    bdpu_guard = CharField(max_length=10, null=True)

    
    
    
    
    
    
    