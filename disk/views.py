from django.shortcuts import render
from disk.models import FileInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, FileResponse,HttpResponseRedirect
import hashlib, os
from disk.utils import fsize

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
    disk_path = 'disk_file'
    if not os.path.exists(disk_path):
        os.mkdir(disk_path)
        
    upfile = request.FILES.get('file', None)
    if not upfile:
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))
    hash_md5 = hashlib.md5(upfile.read()).hexdigest()
    filesize = upfile.size
    filename = upfile.name
    if FileInfo.objects.filter(user=request.user, name=filename, hash_md5=hash_md5):
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))
    file_exist = FileInfo.objects.filter(hash_md5=hash_md5)
    if file_exist:
        FileInfo.objects.get_or_create(name=filename, size=filesize, hash_md5=hash_md5,user=request.user)
        return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))
    des = open(os.path.join(disk_path, hash_md5), 'wb+')
    for chunk in upfile.chunks():
        des.write(chunk)
    des.close()
    FileInfo.objects.get_or_create(name=filename,size=filesize,hash_md5=hash_md5,user=request.user)
    return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))

def file_list(request,user):
    obj = FileInfo.objects.filter(user=request.user.get_username())
    flist = []
    for ob in obj:
        t = {}
        t['user'] = ob.user
        t['name'] = ob.name
        t['size'] = fsize(ob.size)
        t['hash'] = ob.hash_md5
        flist.append(t)
    return render(request,'filelist.html', {'list': flist})

def file_down(request, user, fhash):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    disk_path = 'disk_file'
    file_name = FileInfo.objects.filter(user=user, hash_md5=fhash)[0].name
    res_file = open(os.path.join(disk_path, fhash), 'rb')
    response = HttpResponse(res_file.read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response 

def file_del(request, user, fname):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    hash_md5 = FileInfo.objects.filter(user=user, name=fname)[0].hash_md5
    print(hash_md5)
    count = FileInfo.objects.filter(hash_md5=hash_md5).count()
    print(count)
    if count == 1:
        disk_path = 'disk_file'
        os.remove(os.path.join(disk_path, hash_md5))
        FileInfo.objects.filter(user=user,hash_md5=hash_md5,name=fname).delete()
    else:
        FileInfo.objects.filter(user=user,hash_md5=hash_md5,name=fname).delete()
    return HttpResponseRedirect('/user/{}'.format(request.user.get_username()))

def file_share(request, user, fname, fhash):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    size = FileInfo.objects.filter(user=user,name=fname,hash_md5=fhash)[0].size
    size = fsize(size)
    context = {
        'user': user,
        'name': fname,
        'hash': fhash,
        'size': size,
    }
    print(context)
    return render(request,'share.html',context=context)
