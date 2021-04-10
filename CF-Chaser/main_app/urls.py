from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.logIn, name='login')
]