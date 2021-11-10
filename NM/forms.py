from django.forms import ModelForm
from NM.models import ISR4321, Scripts
from django.views.generic import CreateView

class New_Script(CreateView):
    model = ISR4321
    template_name = 'new_script.html'
    fields = '__all__'

