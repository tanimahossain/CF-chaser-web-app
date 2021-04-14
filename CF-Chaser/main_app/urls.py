from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friendList, name='friendlist'),
    path('chase-by-contest/', views.chaseByContest, name='chasebycontest')
]