from django.forms import ModelForm
from NM.models import Scripts

class ScriptFrom(ModelForm):

    class Meta:
        model = Scripts
        fields = ['script_name', 'host_name', 'banner_motd']
