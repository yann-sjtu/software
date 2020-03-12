from django.urls import path
from . import views

urlpatterns = [
    path(r'^$', views.index),
    path(r'^start/$', views.start),
    path(r'^stop/$', views.stop),
]