from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search , name="search"),
    path("search/<int:distance>/<slug:specialty>/<slug:conditions>/",views.search, name="searchResult"),
    path("login/", views.loginAttempt , name="login"),
    path("logout/", views.logoutAttempt , name="logout"),
    path("changePassword/", views.changePassword , name="changePassword"),
    path("forgotPassword/", views.forgotPassword , name="forgotPassword"),
    path("signup/", views.signup , name="signup"),
    path('endorse/', views.endorse_doctor, name='endorse_doctor'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.update_profile, name='edit_profile'),
    #path('profile/forgot_password/<username>/', views.forgot_password, name='forgot_password'),
]