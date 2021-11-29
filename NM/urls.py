"""NM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from . import views
from . import forms
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    
    #home-page
    path('', views.home, name='home'),
    
    #login-logout
    path('login', views.login_user, name='login'),
    path('login', include('django.contrib.auth.urls')),
    path('logout', views.logout_user, name='Logout'),

    #dashboard
    path('dashboard', views.dashboard, name='Dashboard'),
    path('scripts', views.scripts, name='Scripts'),

    #script-functions
    path('edit_script', views.edit_script, name='Edit Script'),
    path('new_script', views.new_script, name='New Script'),
    path('save', views.save, name='Save'),
    
    #project-functions
    path('save_project', views.save_project, name='Save Project'),

    #generate-functions
    path('generate_text', views.text_generator, name='Generate Text'),
    path('generate_exe', views.exe_generator, name='Generate Executable'),
    
    #statics
    path('devices', views.device_list, name='Devices'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
