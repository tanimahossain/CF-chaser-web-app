from django.shortcuts import render

def registration(request):

    return render(request, 'registration.html')

def logIn(request):

    return render(request, 'login.html')
