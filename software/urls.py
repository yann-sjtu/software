"""software URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from show import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^login/$', views.log_in),
    url(r'^logout/$', views.log_out),
    url(r'^publish/$', views.publish),
    url(r'^upload/$', views.upload),
    url(r'^verify/$', views.verify),
    url(r'^start/$', views.start),
    url(r'^stop/$', views.stop),
    url(r'^score/$', views.score),
    url(r'^buy/$', views.buy),
    
]
