from django.urls import path
from . import views
from django.contrib import admin 
from django.urls import path 
from AppSite import views 

urlpatterns = [
    path("", views.home, name = "home"),
    path("amaan", views.hello, name = "hello"),
    path("register", views.register, name = "register"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path("dashboard", views.Ai_gather, name = "AiScript"),
    path('process_csv/', views.process_csv, name='process_csv'),
    path('api', views.ChartData.as_view()),



]
