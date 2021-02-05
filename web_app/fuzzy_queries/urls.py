from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from fuzzy_queries import views

app_name = "fuzzy_queries"

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("index/", views.welcome, name="welcome"),
    path("index/<str_indices>", views.index, name="index"),
    path("next/<int:ans>/", views.next_suggestion, name="next"),
    path("user_test/", views.user_test, name="user_test"),
    path("user_test_inter/", views.user_test_inter, name="user_test_inter"),
    path("next_results/<str_marks>/", views.next_results, name="next2"),
    path("test_end/", views.user_test_end, name="test_end"),
    # path("user_test_part2/<int:pos>/<ans>", views.user_test_part2, name="user_test_part2"),
    # path("user_test_part2/", views.user_test_inter2, name="user_test_inter2"),
    # path("welcome_3/", views.welcome_3, name="welcome_3"),
    # path("results/", views.results, name="results"),
    # path("", views.index, name="index"),
    # path("test",views.test, name="test")
]