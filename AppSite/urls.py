from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("amaan/", views.hello, name = "hello"),
    path("register/", views.register, name = "register"),
    path("login/", views.login, name = "login"),
    path("page2/", views.page2, name = "page2")
]