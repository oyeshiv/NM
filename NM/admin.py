from django.contrib import admin
from NM.models import ACL_3650, ACL_EL_3650, DHCP_3650, DHCP_EX_C3650, STP_VLAN_3650, VLAN_C3650, WSC3650, CiscoUser, Interface_C3650, OSPFv3_3650, Projects, Devices, DeviceCategories, ISR4321, Scripts

admin.site.register(Devices)
admin.site.register(Projects)
admin.site.register(DeviceCategories)
admin.site.register(Scripts)
admin.site.register(ISR4321)
admin.site.register(WSC3650)
admin.site.register(ACL_3650)
admin.site.register(ACL_EL_3650)
admin.site.register(VLAN_C3650)
admin.site.register(DHCP_3650)
admin.site.register(DHCP_EX_C3650)
admin.site.register(Interface_C3650)
admin.site.register(STP_VLAN_3650)
admin.site.register(CiscoUser)
admin.site.register(OSPFv3_3650)