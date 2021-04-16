from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friendList, name='friendlist'),
    path('chase-by-contest/', views.chaseByContest, name='chasebycontest'),
    path('contest-datails/', views.contestDetails, name='contestdetails'),
    path('addfriend/', views.addFriend, name='addfriend'),
    path('removefriend/', views.removeFriend, name='removefriend'),
    path('contestdetails/<int:contest_id>', views.contestDetails, name='contestdetails'),
]