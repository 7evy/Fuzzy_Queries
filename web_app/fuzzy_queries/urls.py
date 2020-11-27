from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from fuzzy_queries import views

urlpatterns = [
    url(r'^$',views.index),
]