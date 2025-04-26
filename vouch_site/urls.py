from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search , name="search"),
    path("search/<int:distance>/<slug:specialty>/<slug:conditions>/",views.search, name="searchResult"),
    path("login/", views.login , name="login"),
]