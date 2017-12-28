from django.shortcuts import render
from disk.models import FileInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, FileResponse,HttpResponseRedirect

# Create your views here.
def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))
    return render(request,'home.html')

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))
    username = request.POST.get('user',None)
    password = request.POST.get('pass',None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username())) 
    else:
        return HttpResponseRedirect('/')

def user_logout(request):
    if request.user:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def user_sign(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))
    username = request.POST.get('user', None)
    password = request.POST.get('pass', None)
    user = User.objects.create_user(username=username, password=password)
    user.save()
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username())) 
    else:
        return HttpResponseRedirect('/')

def file_upload(request):
    return

def file_list(request,user):

    return render(request,'filelist.html')

def file_down(request):
    return
