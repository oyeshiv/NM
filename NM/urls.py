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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from . import forms
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('router/model-1', views.router_1, name='Router'),
    path('router/model-2', views.router_2, name='Router'),
    path('switch/model-1', views.switch_1, name='Switch'),
    path('switch/model-2', views.switch_2, name='Switch'),
    path('test', views.test, name='Testing'),
    path('index', views.index, name='index'),

    path('home', views.home, name='home'),

    path('home', views.home, name='home'),

    path('base_router', views.base_router, name='base_router'),
    path('form_router', views.form_router, name='form_router'),
    path('base_switch', views.base_switch, name='base_switch'),
    path('base_switch3', views.base_switch3, name='base_switch3'),
    path('form_layer3', views.form_layer3, name='form_layer3'),
    path('form_switch2', views.form_switch2, name='form_switch2')
    
]
