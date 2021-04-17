from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import callerMethods

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
                    if callerMethods.checkUser(request.POST['cfhandle']):
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
                callerMethods.checkDataUpdate(user.username)
                auth.login(request, user)
                return redirect('profile')

            else:
                return render(request, 'login.html', {'error': 'Email and Password do not match'})

        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email is not registered'})

    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logOut(request):
    callerMethods.clearData()
    auth.logout(request)
    return redirect('login')

def Home(request):
    return render(request, 'Homepage.html')

@login_required(login_url='login')
def profile(request):
    detail = callerMethods.getProfileData(request.user.username)
    return render(request, 'Profile.html', {'detail':detail})

@login_required(login_url='login')
def friendList(request):
    msg = callerMethods.massage.msg
    callerMethods.massage.msg = ''
    friends = callerMethods.getFriendListData(request.user.username)

    if len(msg)>0:
        return render(request, 'Friends.html', {'friends':friends, 'msg':msg})
    else:
        return render(request, 'Friends.html', {'friends': friends})


@login_required(login_url='login')
def removeFriend(request):
    username = request.POST['cfHandle']
    action = callerMethods.removeFriend(username, request.user)
    if action:
        msg = 'Friend Successfully Removed'
    else:
        msg = 'CodeForces Handle Does Not Exist in Your Friend List'

    callerMethods.massage.msg = msg
    return redirect('friendlist')

@login_required(login_url='login')
def addFriend(request):
    username = request.POST['cfHandle']
    action = callerMethods.addFriend(username, request.user)
    if action == 1:
        msg = 'Maximum Friend Limit or 20 Reached.'
    elif action == 2:
        msg = 'CodeForces Handle does not Exist.'
    elif action == 3:
        msg = 'CodeForces Handle Already Exists in Your Friend List'
    else:
        msg = 'Friend Added Successfully'

    callerMethods.massage.msg = msg
    return redirect('friendlist')

@login_required(login_url='login')
def chaseByContest(request):
    contests = callerMethods.getChessByContestData(request.user.username)

    paginator = Paginator(contests, 20)
    page_num = request.GET.get('page', 1)

    try:
        details = paginator.page(page_num)
    except PageNotAnInteger:
        details = paginator.page(1)
    except EmptyPage:
        details = paginator.page(paginator.num_pages)

    return render(request, 'Chase By Contest.html', {'contests':details})

@login_required(login_url='login')
def contestDetails(request, contest_id):
    detail, contest_name = callerMethods.getContestDetails(request.user.username, contest_id)
    return render(request, 'contest details.html', {'detail':detail, 'contest_name':contest_name})