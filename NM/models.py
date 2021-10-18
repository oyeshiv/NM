from django.db import models
from django.contrib.postgres.fields import ArrayField

class Ospf(models.Model):
    process_identification = models.CharField(max_length=20)

class CiscoRouterLoginSecutiy(models.Model):
    user_name = models.CharField()
    user_pass = models.CharField()
    login_block_time = models.IntegerField()
    login_tries = models.IntegerField()
    login_tries_time = models.IntegerField()
    login_delay = models.IntegerField()
    login_host = models.IPAddressField()
    login_trap_level = models.CharField()

class CiscoRouterKeyChain(models.Model):
    keychain_name = models.CharField()
    key_string = models.CharField()
    algo = models.CharField()

class CiscoRouterAAA(models.Model):
    radius_server_name = models.CharField()
    server_address = models.IPAddressField()
    radius_pass = models.CharField()
    group_name = models.CharField()
    server_name = models.CharField()

class CiscoRouterZoneSecurity():
    zone_name = models.CharField()
    class_map_name = models.CharField()
    policy_map = models.CharField()
    inspect = models.BooleanField()


class CiscoRouterACL(models.Model):
    acl_name = models.CharField()
    acl_string = models.TextField()

class CiscoRouterSSH(models.Model):
    enable = models.BooleanField()
    ssh_timeout = models.CharField()
    ssh_retries = models.CharField()

class DeviceCategory(models.Model):
    category_name = models.CharField(max_length=100)

class Device(models.Model):
    device_model = models.CharField(max_length=100)
    device_manufacturer = models.CharField(max_length=100)
    router_features = ArrayField(ArrayField(models.ForeignKey(blank=True, size=3), size=8))

    class ISR4321():
        s = models.TextField()
    

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    desc = models.TextField()
    client_name = models.TextField()

class Script(models.Model):
    device = models.ForeignKey(Device)
    script_name = models.CharField()
    host_name = models.CharField()
    domain_name = models.CharField()
    banner_motd = models.CharField()
    en_pass_length = models.CharField()
    en_pass = models.CharField()
    

