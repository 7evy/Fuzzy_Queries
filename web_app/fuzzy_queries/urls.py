from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from fuzzy_queries import views

app_name = "fuzzy_queries"

urlpatterns = [
    path("next/<int:pos>/<int:ans>/", views.next_suggestion, name="next"),
    path("results/", views.results, name="results"),
    path("", views.index, name="index"),
]