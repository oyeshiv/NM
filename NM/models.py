from django.db import models
from django.contrib.postgres.fields import ArrayField

class DeviceCategories(models.Model):
    category_name = models.CharField(max_length=100)

class Devices(models.Model):
    device_category = models.ForeignKey(DeviceCategories, on_delete=models.RESTRICT)
    device_model = models.CharField(max_length=100)
    device_manufacturer = models.CharField(max_length=100)

class Projects(models.Model):
    project_name = models.CharField(max_length=100)
    desc = models.TextField()
    client_name = models.TextField()

class Scripts(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.RESTRICT)
    project = models.ForeignKey(Projects, on_delete=models.RESTRICT)
    date_created = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now_add=True)
    script_name = models.CharField(max_length=100)
    host_name = models.CharField(max_length=100)
    banner_motd = models.TextField(max_length=100)
    

