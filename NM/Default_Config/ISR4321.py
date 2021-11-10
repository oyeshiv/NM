enable 
config t 
hostname @host_name
banner motd # @banner_motd # 
no ip domain lookup 
ip routing 
ipv6 unicast-routing
security passwords min-length @en_pass_length
service password-encryption 
enable algorithm-type sha256 secret @en_pass
username @username algorithm-type scrypt secret @user_pass
line vty 0 4 
exec-timeout 2 0 
login local 
transport input ssh 
exit 
line aux 0 
login local 
exit 
line console 0 
exec-timeout 3 30 
login local 
logging synchronous 
exit 
! 
login block-for @login_block_time attempts @login_tries within @login_tries_time
ip access-list standard @acl_name
@acl_string
exit 
login quiet-mode access-class @acl_name
login delay @login_delay 
login on-success log 
login on-failure log 
security authentication failure rate <threshold-1024> log 
! 
ip domain-name @domain_name
crypto key generate rsa general-keys modulus @ssh_crypto_key  -----------
ip ssh version 2 
ip ssh time-out @ssh_timeout
ip ssh authentication-retries @ssh_retries
! 
logging host @login_host
logging trap @login_trap_level 
logging source-int @login_source -------------
logging on 
! 
no cdp run 
! 
aaa new-model  
radius server <name-SERVER-R> 
address ipv4 <ip address of server- 192.168.0.2> auth-port 1812 acct-port 1813 
key <password-RADPASS> 
exit 
aaa group server radius @radius_group
server name @radius_server_name
aaa local authentication attempts max-fail @max_fail
aaa authentication login default group @radius_group local  
aaa authorization exec default group @radius_group local 
aaa authorization network default group @radius_group local 
aaa accounting exec default start-stop group @radius_group 
aaa accounting network default start-stop group @radius_group
! 
zone security @zone_name
exit 
class-map type inspect match-any @class_map_name
@match_tcp
match protocol tcp
@match_udp
match protocol udp
@match_icmp
match protocol icmp
@match_https
match protocol https
@match_ssh
match protocol ssh
exit 
zone security @zone_internet
! 
policy-map type inspect @policy_map
class type inspect @policy_map
@inspect
inspect 
! 
zone-pair security @policy_map source @zone_name destination @zone_internet
service-policy type inspect @policy_map
exit 
zone-pair security @policy_map source @zone_internet destination @zone_name 
exit 
exit 
!-zone pair may be incorrect in gns3!!! 
fhrp version vrrp v3 
secure boot-image 
secure boot-config 
exit 
copy ru st 
! 
interface g0/0 
ip address @g00_ip @g00_subnet
vrrp @g00_vrrp_num address-family ipv4 
address @g00_vrrp_address    
track @g00_track_num decrement @g00_track_dec
priority @g00_priority
track @g00_track_num decrement @g00_track_dec
exit 
ipv6 enable 
ipv6 address @g00_ipv6_address
ipv6 address @g00_ipv6_link link-local 
vrrp @g00_ipv6_vrrp_num address-family ipv6 
address @g00_ipv6_vrrp_address    
track @g00_ipv6_track_num decrement @g00_ipv6_track_dec
priority @g00_ipv6_priority
track @g00_ipv6_track_num decrement @g00_ipv6_track_dec
exit 
ip nat outside 
zone-member security @zone_internet
crypto map @crypto_map_name NOTE- ipsec needs to be configured first for this int cmd to wrk 
no shutdown 
! 
interface g0/1 
ip address @g01_ip @g01_subnet
ipv6 enable 
ipv6 address @g01_ipv6_address
ipv6 address @g01_ipv6_link link-local 
ospfv3 @g01_ospfv3_ipv4 ipv4 area @g01_ospfv3_area
ospfv3 @g01_ospfv3_ipv6 ipv6 area @g01_ospfv3_ipv6_area
ospfv3 encryption ipsec spi <num-1000> esp <null> sha1 <40-digit number> ----------------------
ip nat inside 
zone-member security @zone_name 
no shutdown 
! 
int g0/2 
ip address @g02_ip @g02_subnet
ipv6 enable 
ipv6 address @g02_ipv6_address
ipv6 address @g02_ipv6_link link-local 
ospfv3 <number> ipv4 area <as-num> 
ospfv3 <number> ipv6 area <as-num> 
ospfv3 encryption ipsec spi <num-1000> esp <null> sha1 <same-40-digit number> 
ip nat inside 
zone-member security <name-INSIDE> 
no shutdown 
!
interface loopback 1 NOTE- different per R router 
ip address <loopback_ip_address-192.168.1.1> <subnet-mask- 255.255.255.255> 
ipv6 enable 
ospfv3 <number> ipv4 area <as-num> 
! 
ip nat pool <name> <start public address> <end public address> netmask <subnet>  
access-list <number> permit <private network address> <wildcard-mask> 
ip nat inside source list <number> pool <name> 
! 
router ospfv3 <number> 
address-family ipv4 unicast 
router-id <id-num> 
redistribute connected 
exit 
address-family ipv6 unicast 
router-id <id-num> 
redistribute connected 
exit 
exit 
! 
ip route <WAN-Loopback-network> <subnet-mask> <next-hop-WAN-int-ip-address> 
ip route <R-opposite-Loopback-network> <subnet-mask> <next-hop-R-int-ip-address> 
! 
ip bgp-community new-format 
route-map <name-NO-EXPORT> 
set community no-export 
! 
router bgp <number> NOTE- AS numbers will be the same for both internal routers 
bgp router-id <id> 
no bgp default ipv4-unicast 
neighbor <WAN-ip address> remote-as <number> 
neighbor <WAN-ip address> update-source Loopback 1  
neighbor <ipv6 address> remote-as <number> 
address-family ipv4 
neighbor <ipv4 address> activate 
network <network address> mask <subnet mask> 
redistribute connected 
neighbor <WAN-ip address> route-map <name-NO-EXPORT> in 
neighbor <WAN-ip address> send-community 
neighbor <ip address of WAN> route-map <name-AS10> out 
exit 
address-family ipv6 
neighbor <ipv6 address> activate 
network <network address/prefix> 
redistribute connected 
neighbor <WAN-ip address> route-map <name-NO-EXPORT> in 
neighbor <WAN-ip address> send-community 
exit 
! 
crypto isakmp enable 
crypto isakmp policy <num-10> 
hash sha 
authentication pre-share 
group 14 
lifetime 3600 
encryption aes 256 
exit 
crypto isakmp key <password-keyacc101> address <remote peer ip adress of WAN-1> 
crypto ipsec transform-set <tag-50> esp-aes 256 esp-sha-hmac 
exit 
crypto ipsec security-association lifetime seconds 3600 
access-list <num-101> permit ip <ip address range of accepted addresses (must suit our addressing scheme)-192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255> 
crypto map <name-CMAP> <num-10> ipsec-isakmp 
match address <acl num-101> 
set peer <WAN-1 peer address> 
set pfs group14 
set transform-set <num-50> 
set security-association lifetime seconds <num-900> 
exit 
!
crypto isakmp policy <num-15> 
authentication pre-share 
hash sha 
group 2
encryption aes 256 
lifetime 3600 
exit
crypto isakmp key <password> address ipv6 <ipv6-address/prefix> 
crypto keyring <name-keyring> 
pre-shared-key address ipv6 <ipv6-address/prefix> key 6 <password-ringpass> 
exit 
crypto ipsec transform-set <name-sercset1> <set> esp-aes 256 esp-sha-hmac 
mode tunnel 
exit 
crypto ipsec profile <name-profile0> 
set transform-set <name-sercset1> 
exit 
crypto isakmp profile <name-profile1> 
self-identify address ipv6 
match identity address ipv6 <WAN-ipv6-address/prefix> 
keyring default 
exit 
interface tunnel @tunnel_num
ipv6 address @tunnel_ipv6_add eui-64 
ipv6 enable 
tunnel source @tunnel_source_interface
tunnel destination @tunnel_destination_address
tunnel mode ipsec ipv6 
tunnel protection ipsec profile @tunnel_protection_profile
end 
! 
clock set @current_time
! 
ntp peer ntp_peer_add
ntp master @ntp_master_num
ntp authenticate 
ntp authentication-key @ntp_auth_key_num md5 @ntp_auth_key_pass
ntp trusted-key @ntp_trust_key
!   
ip prefix-list @ip_prefix_list_name permit @ip_prefix_list_network
! 
route-map @route_map_name permit @route_map_permit_1
match ip address prefix-list @route_map_match_list 
set weight @set_weight
set metric @set_metric
exit 
route-map @route_map_name permit @route_map_permit_2
! 