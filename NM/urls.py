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

    #login-logout
    path('', views.login_user, name='home'),
    path('login', include('django.contrib.auth.urls')),
    path('logout', views.logout_user, name='Logout'),

    #dashboard
    path('dash', views.dash, name='Dashboard'),
    path('scripts', views.scripts, name='Scripts'),

    #script-functions
    path('edit_script', views.edit_script, name='Edit Script'),
    path('new_script', views.new_script, name='New Script'),
    

    #generate-functions
    path('generate_text', views.text_gen, name='Generate Text'),

    #forms
    path('index', views.index, name='index'),
    path('base', views.base, name='Base'),
    path('base_router', views.base_router, name='base_router'),
    path('form_router', views.form_router, name='form_router'),
    path('base_switch', views.base_switch, name='base_switch'),
    path('base_switch3', views.base_switch3, name='base_switch3'),
    path('form_layer3', views.form_layer3, name='form_layer3'),
    path('form_switch2', views.form_switch2, name='form_switch2'),
    path('ISR4321', views.ISR4321, name='ISR4321'),
    path('dynamic_menu', views.dynamic_menu, name='dynamic_menu'),
    path('team', views.team, name='about_us'),

]
