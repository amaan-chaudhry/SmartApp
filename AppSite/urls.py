from django.urls import path
from . import views
from django.contrib import admin 
from django.urls import path 
from AppSite import views 
from django.views.generic import RedirectView
urlpatterns = [
    path("", views.home, name = "home"),
    path("amaan", views.hello, name = "hello"),
    path("register", views.register, name = "register"),
    path("dashboard", views.dashboard, name = "dashboard"),
    path('process_csv/', views.process_csv, name='process_csv'),
    path('api', views.ChartData.as_view()),
    path('oursolution', views.oursolution),
    path('contactus', views.contact),
    path('features', views.features),
    path('security', views.security),
    path('about', views.about),
    path('authenicate/', views.authenicate_user, name= "authenicate"),
    path('acquirer/', views.Ai_interface, name = "acquirer"),
 

]
