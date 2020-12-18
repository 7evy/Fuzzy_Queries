from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from fuzzy_queries import views

app_name = "fuzzy_queries"

urlpatterns = [
    path("next/<int:pos>/<int:ans>/", views.next_suggestion, name="next"),
    path("user_test/", views.user_test, name="user_test"),
    path("user_test_inter/<str_marks>", views.user_test_inter, name="user_test_inter"),
    path("user_test_part2/<int:pos>/<ans>", views.user_test_part2, name="user_test_part2"),
    # path("results/", views.results, name="results"),
    path("", views.index, name="index"),
]