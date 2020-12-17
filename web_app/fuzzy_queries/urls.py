from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from fuzzy_queries import views

app_name = "fuzzy_queries"

urlpatterns = [
    path("next/<int:pos>/<int:ans>/", views.next_suggestion, name="next"),
    path("user_test/", views.user_test, name="user_test"),
    path("user_test_part2/<str_marks>", views.user_test_part2, name="user_test_part2"),
    # path("results/", views.results, name="results"),
    path("", views.index, name="index"),
    path("test",views.test, name="test")
]