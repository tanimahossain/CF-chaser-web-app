from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from . import checker


def registration(request):

    if request.method == 'POST':
        if request.POST['email'] and request.POST['cfhandle'] and request.POST['password'] and request.POST['confpassword']:
            try:
                User.objects.get(username=request.POST['cfhandle'])
                return render(request, 'registration.html', {'error':'User already exists'})

            except User.DoesNotExist:
                try:
                    User.objects.get(email=request.POST['email'])
                    return render(request, 'registration.html', {'error': 'Email already exists'})

                except User.DoesNotExist:
                    if checker.checkUser(request.POST['cfhandle']):
                        if request.POST['password'] == request.POST['confpassword']:
                            user = User.objects.create_user(username=request.POST['cfhandle'], password=request.POST['password'], email=request.POST['email'])
                            auth.login(request, user)

                            return redirect('profile')

                        else:
                            return render(request, 'registration.html', {'error': 'Passwords do not match'})

                    else:
                        return render(request, 'registration.html', {'error': 'CodeForces Handle does not exist'})

        else:
            return render(request, 'registration.html', {'error':'Please Fill Up all the Information'})

    else:
        return render(request, 'registration.html')

def logIn(request):

    if request.method == 'POST':

        try:
            user = User.objects.get(email=request.POST['email'])
            user = auth.authenticate(username=user.username, password=request.POST['password'])

            if user is not None:
                auth.login(request, user)
                return redirect('profile')
            else:
                return render(request, 'login.html', {'error': 'Email and Password do not match'})

        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email is not registered'})

    else:
        return render(request, 'login.html')

def logOut(request):
    auth.logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'Profile.html')

